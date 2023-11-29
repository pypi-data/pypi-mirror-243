import json
import graphviz
import pandas as pd
import datetime
import warnings
from uuid import UUID

from sempy.fabric._dataframe._fabric_dataframe import FabricDataFrame
from sempy.fabric._client import DatasetXmlaClient, DatasetRestClient
from sempy.fabric._client._pbi_rest_api import _PBIRestAPI
from sempy.fabric._client._refresh_execution_details import RefreshExecutionDetails
from sempy.fabric._client._connection_mode import parse_connection_mode, ConnectionMode
from sempy.fabric._cache import _get_or_create_workspace_client
from sempy.fabric._trace._trace_connection import TraceConnection
from sempy.fabric._trace._trace import Trace
from sempy.fabric._utils import _get_relationships, dotnet_to_pandas_date, collection_to_dataframe
from sempy._utils._pandas_utils import rename_and_validate_from_records
from sempy.relationships import plot_relationship_metadata
from sempy.relationships._utils import _to_dataframe_dict
from sempy.relationships._validate import _list_relationship_violations
from sempy._utils._log import log, log_tables
from sempy.fabric._token_provider import SynapseTokenProvider

from typing import Dict, List, Optional, Union, Tuple


@log
def execute_tmsl(script: Union[Dict, str], refresh_tom_cache: bool = True, workspace: Optional[Union[str, UUID]] = None):
    """
    Execute TMSL script.

    Parameters
    ----------
    script : Dict or str
        The TMSL script json.
    refresh_tom_cache : bool, default=True
        Whether or not to refresh the dataset after executing the TMSL script.
    workspace : str or uuid.UUID, default=None
        The Fabric workspace name or UUID object containing the workspace ID.
        Defaults to None which resolves to the workspace of the attached lakehouse
        or if no lakehouse attached, resolves to the workspace of the notebook.
    """
    if isinstance(script, Dict):
        script = json.dumps(script)

    workspace_client = _get_or_create_workspace_client(workspace)
    workspace_client.execute_tmsl(script)

    if refresh_tom_cache:
        workspace_client.refresh_tom_cache()


@log
def refresh_tom_cache(workspace: Optional[Union[str, UUID]] = None):
    """
    Refresh TOM cache in the notebook kernel.

    Parameters
    ----------
    workspace : str or uuid.UUID, default=None
        The Fabric workspace name or UUID object containing the workspace ID.
        Defaults to None which resolves to the workspace of the attached lakehouse
        or if no lakehouse attached, resolves to the workspace of the notebook.
    """
    _get_or_create_workspace_client(workspace).refresh_tom_cache()


@log
def get_roles(dataset: Union[str, UUID], include_members: bool = False, workspace: Optional[Union[str, UUID]] = None) -> pd.DataFrame:
    """
    Retrieve all roles associated with the dataset.

    Parameters
    ----------
    dataset : str or uuid.UUID
        Name or UUID of the dataset.
    include_members : bool, default=False
        Whether or not to include members for each role.
    workspace : str or uuid.UUID, default=None
        The Fabric workspace name or UUID object containing the workspace ID.
        Defaults to None which resolves to the workspace of the attached lakehouse
        or if no lakehouse attached, resolves to the workspace of the notebook.

    Returns
    -------
    pandas.DataFrame
        Dataframe listing roles and with their attributes.
    """
    workspace_client = _get_or_create_workspace_client(workspace)
    model = workspace_client.get_dataset(dataset).Model

    extraction_def = [
        ("Role",                  lambda r: r[0].Name,                                "str"),   # noqa: E272
        ("Description",           lambda r: r[0].Description,                         "str"),   # noqa: E272
        ("Model Permission",      lambda r: r[0].ModelPermission.ToString(),          "str"),   # noqa: E272
        ("Modified Time",         lambda r: dotnet_to_pandas_date(r[0].ModifiedTime), "datetime64[ns]"),  # noqa: E272
    ]

    if include_members:
        extraction_def.append(("Member", lambda r: r[1].Name, "str"))

        collection = [(r, m) for r in model.Roles for m in r.Members]
    else:
        collection = [(r, None) for r in model.Roles]

    return collection_to_dataframe(collection, extraction_def)


@log
def get_row_level_security_permissions(dataset: Union[str, UUID], workspace: Optional[Union[str, UUID]] = None) -> pd.DataFrame:
    """
    Retrieve row level security permissions for a dataset.

    Parameters
    ----------
    dataset : str or uuid.UUID
        Name or UUID of the dataset.
    workspace : str or uuid.UUID, default=None
        The Fabric workspace name or UUID object containing the workspace ID.
        Defaults to None which resolves to the workspace of the attached lakehouse
        or if no lakehouse attached, resolves to the workspace of the notebook.

    Returns
    -------
    pandas.DataFrame
        Dataframe listing tables and row filter expressions (DAX) for the dataset.
    """
    workspace_client = _get_or_create_workspace_client(workspace)
    model = workspace_client.get_dataset(dataset).Model

    # (role, table_permission)
    extraction_def = [
        ("Role",              lambda r: r[0].Name,             "str"),   # noqa: E272
        ("Table",             lambda r: r[1].Name,             "str"),   # noqa: E272
        ("Filter Expression", lambda r: r[1].FilterExpression, "str"),   # noqa: E272
    ]

    collection = [
        (role, table_permission)
        for role in model.Roles
        for table_permission in role.TablePermissions
    ]

    return collection_to_dataframe(collection, extraction_def)


@log
def list_hierarchies(dataset: Union[str, UUID], workspace: Optional[Union[str, UUID]] = None) -> pd.DataFrame:
    """
    List hierarchies in a dataset.

    Parameters
    ----------
    dataset : str or uuid.UUID
        Name or UUID of the dataset.
    workspace : str or uuid.UUID, default=None
        The Fabric workspace name or UUID object containing the workspace ID.
        Defaults to None which resolves to the workspace of the attached lakehouse
        or if no lakehouse attached, resolves to the workspace of the notebook.

    Returns
    -------
    pandas.DataFrame
        Dataframe listing the hierachies and their attributes.
    """
    workspace_client = _get_or_create_workspace_client(workspace)
    database = workspace_client.get_dataset(dataset).Model

    # see https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.level?view=analysisservices-dotnet
    # (table, hierarchy, level)
    extraction_def = [
        ("Table Name",            lambda r: r[0].Name,        "str"),    # noqa: E272
        ("Column Name",           lambda r: r[2].Column.Name, "str"),    # noqa: E272
        ("Hiearchy Name",         lambda r: r[1].Name,        "str"),    # noqa: E272
        ("Hierarchy Description", lambda r: r[1].Description, "str"),    # noqa: E272
        ("Hierarchy Hidden",      lambda r: r[1].IsHidden,    "bool"),   # noqa: E272
        ("Hierarchy State",       lambda r: r[1].State,       "str"),    # noqa: E272
        ("Level Name",            lambda r: r[2].Name,        "str"),    # noqa: E272
        ("Level Description",     lambda r: r[2].Description, "str"),    # noqa: E272
        ("Level Ordinal",         lambda r: r[2].Ordinal,     "Int64"),  # noqa: E272
    ]

    collection = [
        (table, hierarchy, level)
        for table in database.Model.Tables
        for hierarchy in table.Hierarchies
        for level in hierarchy.Levels
    ]

    return collection_to_dataframe(collection, extraction_def)


@log
def list_datasets(workspace: Optional[Union[str, UUID]] = None, mode: str = "xmla") -> pd.DataFrame:
    """
    List datasets in a `Fabric workspace <https://learn.microsoft.com/en-us/fabric/get-started/workspaces>`_.

    Parameters
    ----------
    workspace : str or uuid.UUID, default=None
        The Fabric workspace name or UUID object containing the workspace ID.
        Defaults to None which resolves to the workspace of the attached lakehouse
        or if no lakehouse attached, resolves to the workspace of the notebook.
    mode : str, default="xmla"
        Whether to use the XMLA "xmla" or REST API "rest".
        See `REST docs <https://learn.microsoft.com/en-us/rest/api/power-bi/datasets/get-datasets>`_ for returned fields.

    Returns
    -------
    pandas.DataFrame
        Dataframe listing databases and their attributes.
    """
    return _get_or_create_workspace_client(workspace).get_datasets(mode)


@log
def list_measures(dataset: Union[str, UUID], workspace: Optional[Union[str, UUID]] = None) -> pd.DataFrame:
    """
    Retrieve all measures associated with the given dataset.

    Parameters
    ----------
    dataset : str or uuid.UUID
        Name or UUID of the dataset.
    workspace : str or uuid.UUID, default=None
        The Fabric workspace name or UUID object containing the workspace ID.
        Defaults to None which resolves to the workspace of the attached lakehouse
        or if no lakehouse attached, resolves to the workspace of the notebook.

    Returns
    -------
    pandas.DataFrame
        Dataframe listing measures and their attributes.
    """
    return _get_or_create_workspace_client(workspace).list_measures(dataset)


@log
def refresh_dataset(
    dataset: Union[str, UUID],
    workspace: Optional[Union[str, UUID]] = None,
    refresh_type: str = "automatic",
    max_parallelism: int = 10,
    commit_mode: str = "transactional",
    retry_count: int = 0,
    objects: Optional[List] = None,
    apply_refresh_policy: bool = True,
    effective_date: datetime.date = datetime.date.today(),
    verbose: int = 0
) -> str:
    """
    Refresh data associated with the given dataset.

    For detailed documentation on the implementation see
    `Enhanced refresh with the Power BI REST API <https://learn.microsoft.com/en-us/power-bi/connect-data/asynchronous-refresh>`_.

    Parameters
    ----------
    dataset : str or uuid.UUID
        Name or UUID of the dataset.
    workspace : str or uuid.UUID, default=None
        The Fabric workspace name or UUID object containing the workspace ID.
        Defaults to None which resolves to the workspace of the attached lakehouse
        or if no lakehouse attached, resolves to the workspace of the notebook.
    refresh_type : str, default="automatic"
        The type of processing to perform. Types align with the TMSL refresh command types: full,
        clearValues, calculate, dataOnly, automatic, and defragment. The add type isn't supported.
        Defaults to "automatic".
    max_parallelism : int, default=10
        Determines the maximum number of threads that can run the processing commands in parallel.
        This value aligns with the MaxParallelism property that can be set in the TMSL Sequence
        command or by using other methods. Defaults to 10.
    commit_mode : str, default="transactional"
        Determines whether to commit objects in batches or only when complete.
        Modes are "transactional" and "partialBatch". Defaults to "transactional".
    retry_count : int, default=0
        Number of times the operation retries before failing. Defaults to 0.
    objects : List, default=None
        A list of objects to process. Each object includes table when processing an entire table,
        or table and partition when processing a partition. If no objects are specified,
        the entire dataset refreshes. Pass output of json.dumps of a structure that specifies the
        objects that you want to refresh. For example, this is to refresh "DimCustomer1" partition
        of table "DimCustomer" and complete table "DimDate"::

            [
                {
                    "table": "DimCustomer",
                    "partition": "DimCustomer1"
                },
                {
                    "table": "DimDate"
                }
            ]

    apply_refresh_policy : bool, default=True
        If an incremental refresh policy is defined, determines whether to apply the policy.
        Modes are true or false. If the policy isn't applied, the full process leaves partition
        definitions unchanged, and fully refreshes all partitions in the table. If commitMode is
        transactional, applyRefreshPolicy can be true or false. If commitMode is partialBatch,
        applyRefreshPolicy of true isn't supported, and applyRefreshPolicy must be set to false.
    effective_date : datetime.date, default=datetime.date.today()
        If an incremental refresh policy is applied, the effectiveDate parameter overrides the current date.
    verbose : int
        If set to non-zero, extensive log output is printed.

    Returns
    -------
    str
        The refresh request id.
    """
    client: DatasetRestClient = _get_or_create_workspace_client(workspace).get_dataset_client(dataset)  # type: ignore
    poll_url = client.refresh_async(refresh_type, max_parallelism, commit_mode, retry_count, objects,
                                    apply_refresh_policy, effective_date, verbose)

    # extract the refresh request id from the poll url
    return poll_url.split("/")[-1]


@log
def list_refresh_requests(
        dataset: Union[str, UUID],
        workspace: Optional[Union[str, UUID]] = None,
        top_n: Optional[int] = None
) -> pd.DataFrame:
    """
    Poll the status or refresh requests for a given dataset using Enhanced refresh with the Power BI REST API.

    See details in: `PBI Documentation <https://learn.microsoft.com/en-us/power-bi/connect-data/asynchronous-refresh>`_

    Parameters
    ----------
    dataset : str or uuid.UUID
        Name or UUID of the dataset.
    workspace : str or uuid.UUID, default=None
        The Fabric workspace name or UUID object containing the workspace ID.
        Defaults to None which resolves to the workspace of the attached lakehouse
        or if no lakehouse attached, resolves to the workspace of the notebook.
    top_n : int, default = None
        Limit the number of refresh operations returned.

    Returns
    -------
    pandas.DataFrame:
        Dataframe with statuses of refresh request retrieved based on the passed parameters.
    """
    client: DatasetRestClient = _get_or_create_workspace_client(workspace).get_dataset_client(dataset)  # type: ignore
    return client.list_refresh_history(top_n=top_n)


@log
def get_refresh_execution_details(
        dataset: Union[str, UUID],
        refresh_request_id: Union[str, UUID],
        workspace: Optional[Union[str, UUID]] = None,
) -> RefreshExecutionDetails:
    """
    Poll the status for a specific refresh requests using Enhanced refresh with the Power BI REST API.

    More details on the underlying implementation in `PBI Documentation <https://learn.microsoft.com/en-us/power-bi/connect-data/asynchronous-refresh>`_

    Parameters
    ----------
    dataset : str or uuid.UUID
        Name or UUID of the dataset.
    refresh_request_id : str or uuid.UUID
        Id of refresh request on which to check the status.
    workspace : str or uuid.UUID, default=None
        The Fabric workspace name or UUID object containing the workspace ID.
        Defaults to None which resolves to the workspace of the attached lakehouse
        or if no lakehouse attached, resolves to the workspace of the notebook.

    Returns
    -------
    RefreshExecutionDetails:
        RefreshExecutionDetails instance with statuses of refresh request retrieved based on the passed URL.
    """
    client: DatasetRestClient = _get_or_create_workspace_client(workspace).get_dataset_client(dataset)  # type: ignore
    return client.get_refresh_execution_details(refresh_request_id)


@log
def read_table(
    dataset: Union[str, UUID],
    table: str,
    fully_qualified_columns: bool = False,
    num_rows: Optional[int] = None,
    multiindex_hierarchies: bool = False,
    mode: str = "xmla",
    workspace: Optional[Union[str, UUID]] = None,
    verbose: int = 0
) -> FabricDataFrame:
    """
    Read a PowerBI table into a FabricDataFrame.

    Parameters
    ----------
    dataset : str or uuid.UUID
        Name or UUID of the dataset.
    table : str
        Name of the table to read.
    fully_qualified_columns : bool, default=False
        Whether or not to represent columns in their fully qualified form (TableName[ColumnName]).
    num_rows : int, default=None
        How many rows of the table to return. If None, all rows are returned.
    multiindex_hierarchies : bool, default=False
        Whether or not to convert existing `PowerBI Hierarchies <https://learn.microsoft.com/en-us/power-bi/create-reports/service-metrics-get-started-hierarchies>`_
        to pandas MultiIndex.
    mode : str, default="xmla"
        Whether to use the XMLA "xmla", REST API "rest", export of import datasets to Onelake "onelake" to retrieve the data.
    workspace : str or uuid.UUID, default=None
        The Fabric workspace name or UUID object containing the workspace ID. Defaults to None which resolves to the workspace of the attached lakehouse
        or if no lakehouse attached, resolves to the workspace of the notebook.
    verbose : int
        Verbosity. 0 means no verbosity.

    Returns
    -------
    FabricDataFrame
        Dataframe for the given table name with metadata from the PowerBI model.
    """  # noqa E501

    conn_mode = parse_connection_mode(mode)

    return _get_or_create_workspace_client(workspace) \
        .get_dataset_client(dataset, mode=conn_mode) \
        .read_table(table, fully_qualified_columns, num_rows, multiindex_hierarchies, verbose=verbose)


@log
def get_tmsl(dataset: Union[str, UUID], workspace: Optional[Union[str, UUID]] = None) -> str:
    """
    Retrieve the Tabular Model Scripting Language (`TMSL <https://learn.microsoft.com/en-us/analysis-services/tmsl/tabular-model-scripting-language-tmsl-reference?view=asallproducts-allversions>`_) for a given dataset.

    Parameters
    ----------
    dataset : str or uuid.UUID
        Name or UUID of the dataset.
    workspace : str or uuid.UUID, default=None
        The Fabric workspace name or UUID object containing the workspace ID. Defaults to None which resolves to the workspace of the attached lakehouse
        or if no lakehouse attached, resolves to the workspace of the notebook.

    Returns
    -------
    str
        `TMSL <https://learn.microsoft.com/en-us/analysis-services/tmsl/tabular-model-scripting-language-tmsl-reference?view=asallproducts-allversions>`_ for the given dataset.
    """ # noqa E501
    workspace_client = _get_or_create_workspace_client(workspace)
    return workspace_client.get_tmsl(dataset)


@log
def list_tables(
    dataset: Union[str, UUID],
    include_columns: bool = False,
    include_partitions: bool = False,
    workspace: Optional[Union[str, UUID]] = None
) -> pd.DataFrame:
    """
    List all tables in a dataset.

    Parameters
    ----------
    dataset : str or uuid.UUID
        Name or UUID of the dataset.
    include_columns : bool, default=False
        Whether or not to include column level information.
        Cannot be combined with include_partitions.
    include_partitions : bool, default=False
        Whether or not to include partition level information.
        Cannot be combined with include_columns.
    workspace : str or uuid.UUID, default=None
        The Fabric workspace name or UUID object containing the workspace ID.
        Defaults to None which resolves to the workspace of the attached lakehouse
        or if no lakehouse attached, resolves to the workspace of the notebook.

    Returns
    -------
    pandas.DataFrame
        Dataframe listing the tables and optional columns.
    """
    if include_columns and include_partitions:
        raise ValueError("Cannot include both columns and partitions.")

    workspace_client = _get_or_create_workspace_client(workspace)
    tabular_database = workspace_client.get_dataset(dataset)

    def table_type(t):
        if t.CalculationGroup is not None:
            return "Calculation Group"
        elif any(p.SourceType == "Calculated" for p in t.Partitions):
            return "Calculated Table"
        else:
            return "Table"

    extraction_def = [
        ("Name",          lambda t: t.Name,         "str"),   # noqa: E272
        ("Description",   lambda t: t.Description,  "str"),   # noqa: E272
        ("Hidden",        lambda t: t.IsHidden,     "bool"),  # noqa: E272
        ("Data Category", lambda t: t.DataCategory, "str"),   # noqa: E272
        ("Type",          table_type,               "str"),   # noqa: E272
    ]

    if include_partitions:
        warnings.warn(DeprecationWarning("This option will be removed in a future release. Please use list_partitions instead."))
        extraction_def.extend([
            ("Partition Name",           lambda t: [p.Name for p in t.Partitions],    "object"),  # noqa: E272
            ("Partition Refreshed Time", lambda t: [
                    dotnet_to_pandas_date(p.RefreshedTime)
                    for p in t.Partitions
                ],                                                                    "datetime64[ns]"),
        ])

    if include_columns:
        warnings.warn(DeprecationWarning("This option will be removed in a future release. Please use list_columns instead."))
        extraction_def.extend([
            ("Column", lambda t: [c.Name for c in t.Columns if not c.Name.startswith("RowNumber")], "object")
        ])

    collection = filter(lambda t: not workspace_client._is_internal(t), tabular_database.Model.Tables)

    df = collection_to_dataframe(collection, extraction_def)

    if include_columns:
        df = df.explode("Column")
    if include_partitions:
        df = df.explode(["Partition Name", "Partition Refreshed Time"])

    return df


@log
def list_columns(
    dataset: Union[str, UUID],
    table: Optional[str] = None,
    workspace: Optional[Union[str, UUID]] = None
) -> pd.DataFrame:
    """
    List all columns for all tables in a dataset.

    Parameters
    ----------
    dataset : str or uuid.UUID
        Name or UUID of the dataset.
    table : str, default=None
        Name of the table.
    workspace : str or uuid.UUID, default=None
        The Fabric workspace name or UUID object containing the workspace ID.
        Defaults to None which resolves to the workspace of the attached lakehouse
        or if no lakehouse attached, resolves to the workspace of the notebook.

    Returns
    -------
    pandas.DataFrame
        Dataframe listing the columns.
    """
    import Microsoft.AnalysisServices.Tabular as TOM

    workspace_client = _get_or_create_workspace_client(workspace)
    tabular_database = workspace_client.get_dataset(dataset)

    def source(column) -> Optional[str]:
        if column.Type == TOM.ColumnType.Calculated:
            return column.Expression
        elif column.Type in [TOM.ColumnType.Data, TOM.ColumnType.CalculatedTableColumn]:
            return column.SourceColumn

        return None

    def sort_by_column(column) -> Optional[str]:
        if column.SortByColumn is None:
            return None
        else:
            return column.SortByColumn.Name

    # see https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.column?view=analysisservices-dotnet
    # see https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.calculatedcolumn?view=analysisservices-dotnet
    # see https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.datacolumn?view=analysisservices-dotnet
    # table, column
    extraction_def = [
        ("Table Name",          lambda r: r[0].Name,                    "str"),   # noqa: E272
        ("Column Name",         lambda r: r[1].Name,                    "str"),   # noqa: E272
        ("Description",         lambda r: r[1].Description,             "str"),   # noqa: E272
        ("Type",                lambda r: r[1].Type.ToString(),         "str"),   # noqa: E272
        ("Data Type",           lambda r: r[1].DataType.ToString(),     "str"),   # noqa: E272
        ("Hidden",              lambda r: r[1].IsHidden,                "str"),   # noqa: E272
        ("Format String",       lambda r: r[1].FormatString,            "str"),   # noqa: E272
        ("Source",              lambda r: source(r[1]),                 "str"),   # noqa: E272
        ("Data Category",       lambda r: r[1].DataCategory,            "str"),   # noqa: E272
        ("Display Folder",      lambda r: r[1].DisplayFolder,           "str"),   # noqa: E272
        ("Key",                 lambda r: r[1].IsKey,                   "bool"),  # noqa: E272
        ("Unique",              lambda r: r[1].IsUnique,                "bool"),  # noqa: E272
        ("Sort By Column",      lambda r: sort_by_column(r[1]),         "str"),   # noqa: E272
        ("Summarize By",        lambda r: r[1].SummarizeBy.ToString(),  "str"),   # noqa: E272
        ("Is Available in MDX", lambda r: r[1].IsAvailableInMDX,        "bool"),  # noqa: E272
        ("Encoding Hint",       lambda r: r[1].EncodingHint.ToString(), "str"),   # noqa: E272
        ("State",               lambda r: r[1].State.ToString(),        "str"),   # noqa: E272
        ("Error Message",       lambda r: r[1].ErrorMessage,            "str"),   # noqa: E272
        ("Modified Time",       lambda r: dotnet_to_pandas_date(r[1].ModifiedTime), "datetime64[ns]"),  # noqa: E272
    ]

    collection = [
        (table_obj, column)
        for table_obj in tabular_database.Model.Tables
        # filter internals
        if not workspace_client._is_internal(table_obj)
        # filter by table name
        if table is None or table_obj.Name == table
        for column in table_obj.Columns
        # filter auto-generated RowNumber
        if not column.Name.startswith("RowNumber")
    ]

    df = collection_to_dataframe(collection, extraction_def)

    return df


@log
def list_translations(
    dataset: Union[str, UUID],
    workspace: Optional[Union[str, UUID]] = None
) -> pd.DataFrame:
    """
    List all translations in a dataset.

    Parameters
    ----------
    dataset : str or uuid.UUID
        Name or UUID of the dataset.
    workspace : str or uuid.UUID, default=None
        The Fabric workspace name or UUID object containing the workspace ID.
        Defaults to None which resolves to the workspace of the attached lakehouse
        or if no lakehouse attached, resolves to the workspace of the notebook.

    Returns
    -------
    pandas.DataFrame
        Dataframe listing the translations.
    """
    import Microsoft.AnalysisServices.Tabular as TOM

    workspace_client = _get_or_create_workspace_client(workspace)
    database = workspace_client.get_dataset(dataset)

    # https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.culture?view=analysisservices-dotnet
    # (culture, object_translation)
    def table_name(r):
        if r[1].Object.ObjectType == TOM.ObjectType.Table:
            return r[1].Object.Name
        else:
            return r[1].Object.Table.Name

    extraction_def = [
        ("Culture Name",  lambda r: r[0].Name,                                "str"),             # noqa: E272
        ("Table Name",    table_name,                                         "str"),             # noqa: E272
        ("Object Name",   lambda r: r[1].Object.Name,                         "str"),             # noqa: E272
        ("Object Type",   lambda r: r[1].Object.ObjectType.ToString(),        "str"),             # noqa: E272
        ("Translation",   lambda r: r[1].Value,                               "str"),             # noqa: E272
        ("Property",      lambda r: r[1].Property.ToString(),                 "str"),             # noqa: E272
        ("Modified Time", lambda r: dotnet_to_pandas_date(r[1].ModifiedTime), "datetime64[ns]"),  # noqa: E272
    ]

    collection = [
        (culture, object_translation)
        for culture in database.Model.Cultures
        for object_translation in culture.ObjectTranslations
    ]

    return collection_to_dataframe(collection, extraction_def)


@log
def list_expressions(
    dataset: Union[str, UUID],
    workspace: Optional[Union[str, UUID]] = None
) -> pd.DataFrame:
    """
    List all expressions in a dataset.

    Parameters
    ----------
    dataset : str or uuid.UUID
        Name or UUID of the dataset.
    workspace : str or uuid.UUID, default=None
        The Fabric workspace name or UUID object containing the workspace ID.
        Defaults to None which resolves to the workspace of the attached lakehouse
        or if no lakehouse attached, resolves to the workspace of the notebook.

    Returns
    -------
    pandas.DataFrame
        Dataframe listing the expressions.
    """
    workspace_client = _get_or_create_workspace_client(workspace)
    database = workspace_client.get_dataset(dataset)

    # see https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.namedexpressioncollection?view=analysisservices-dotnet
    extraction_def = [
        ("Name",          lambda r: r.Name,                                "str"),   # noqa: E272
        ("Description",   lambda r: r.Description,                         "str"),   # noqa: E272
        ("Expression",    lambda r: r.Expression,                          "str"),   # noqa: E272
        ("Kind",          lambda r: r.Kind.ToString(),                     "str"),   # noqa: E272
        ("M Attributes",  lambda r: r.MAttributes,                         "str"),   # noqa: E272
        ("Modified Time", lambda r: dotnet_to_pandas_date(r.ModifiedTime), "datetime64[ns]"),  # noqa: E272
    ]

    return collection_to_dataframe(database.Model.Expressions, extraction_def)


@log
def list_partitions(
    dataset: Union[str, UUID],
    table: Optional[str] = None,
    workspace: Optional[Union[str, UUID]] = None
) -> pd.DataFrame:
    """
    List all partitions in a dataset.

    Parameters
    ----------
    dataset : str or uuid.UUID
        Name or UUID of the dataset.
    table : str, default=None
        Name of the table.
    workspace : str or uuid.UUID, default=None
        The Fabric workspace name or UUID object containing the workspace ID.
        Defaults to None which resolves to the workspace of the attached lakehouse
        or if no lakehouse attached, resolves to the workspace of the notebook.

    Returns
    -------
    pandas.DataFrame
        Dataframe listing the partitions.
    """
    import Microsoft.AnalysisServices.Tabular as TOM

    workspace_client = _get_or_create_workspace_client(workspace)
    database = workspace_client.get_dataset(dataset)

    def query(partition):
        if partition.SourceType in [TOM.PartitionSourceType.M, TOM.PartitionSourceType.Calculated]:
            # https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.mpartitionsource?view=analysisservices-dotnet
            # https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.calculatedpartitionsource?view=analysisservices-dotnet
            return partition.Source.Expression
        elif partition.SourceType == TOM.PartitionSourceType.Query:
            # https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.querypartitionsource?view=analysisservices-dotnet
            return partition.Source.Query
        elif partition.SourceType == TOM.PartitionSourceType.Entity:
            # https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.entitypartitionsource?view=analysisservices-dotnet
            return partition.Source.EntityName
        else:
            # CalculationGroup, Inferred, ...
            return None

    def query_group(partition):
        if partition.QueryGroup is None:
            return None
        else:
            return partition.QueryGroup.Name

    # see https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.partition?view=analysisservices-dotnet
    # (table, partition)
    extraction_def = [
        ("Table Name",     lambda r: r[0].Name,                                 "str"),   # noqa: E272
        ("Partition Name", lambda r: r[1].Name,                                 "str"),   # noqa: E272
        ("Description",    lambda r: r[1].Description,                          "str"),   # noqa: E272
        ("Error Message",  lambda r: r[1].ErrorMessage,                         "str"),   # noqa: E272
        ("Mode",           lambda r: r[1].Mode.ToString(),                      "str"),   # noqa: E272
        ("Data View",      lambda r: r[1].DataView.ToString(),                  "str"),   # noqa: E272
        ("Source Type",    lambda r: r[1].SourceType.ToString(),                "str"),   # noqa: E272
        ("Query",          lambda r: query(r[1]),                               "str"),   # noqa: E272
        ("Query Group",    lambda r: query_group(r[1]),                         "str"),   # noqa: E272
        ("Refreshed Time", lambda r: dotnet_to_pandas_date(r[1].RefreshedTime), "datetime64[ns]"),  # noqa: E272
        ("Modified Time",  lambda r: dotnet_to_pandas_date(r[1].ModifiedTime),  "datetime64[ns]"),  # noqa: E272
    ]

    collection = [
        (table_obj, partition)
        for table_obj in database.Model.Tables
        # filter by table name
        if table is None or table_obj.Name == table
        for partition in table_obj.Partitions
    ]

    return collection_to_dataframe(collection, extraction_def)


@log
def evaluate_measure(
    dataset: Union[str, UUID],
    measure: Union[str, List[str]],
    groupby_columns: Optional[List[str]] = None,
    filters: Optional[Dict[str, List[str]]] = None,
    fully_qualified_columns: Optional[bool] = None,
    num_rows: Optional[int] = None,
    use_xmla: bool = False,
    workspace: Optional[Union[str, UUID]] = None,
    verbose: int = 0
) -> FabricDataFrame:
    """
    Compute PowerBI `measure <https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-measures>`_ for a given dataset.

    Parameters
    ----------
    dataset : str or uuid.UUID
        Name or UUID of the dataset.
    measure : str or list of str
        Name of the measure, or list of measures to compute.
    groupby_columns : list, default=None
        List of columns in a fully qualified form e.g. "TableName[ColumnName]" or "'Table Name'[Column Name]".
    filters : dict, default=None
        Dictionary containing a list of column values to filter the output by, where
        the key is a column reference, which must be fully qualified with the table name.
        Currently only supports the "in" filter. For example, to specify that in the "State" table
        the "Region" column can only be "East" or "Central" and that the "State" column
        can only be "WA" or "CA"::

            {
                "State[Region]":    ["East", "Central"],
                "State[State]":     ["WA", "CA"]
            }

    fully_qualified_columns : bool, default=None
        Whether to output columns in their fully qualified form (TableName[ColumnName] for dimensions).
        Measures are always represented without the table name.
        If None, the fully qualified form will only be used if there is a name conflict between columns from different tables.
    num_rows : int, default=None
        How many rows of the table to return. If None, all rows are returned.
    use_xmla : bool, default=False
        Whether or not to use `XMLA <https://learn.microsoft.com/en-us/analysis-services/xmla/xml-for-analysis-xmla-reference?view=asallproducts-allversions>`_ 
        as the backend for evaluation. When False, REST backend will be used.
    workspace : str or uuid.UUID, default=None
        The Fabric workspace name or UUID object containing the workspace ID.
        Defaults to None which resolves to the workspace of the attached lakehouse
        or if no lakehouse attached, resolves to the workspace of the notebook.
    verbose : int
        Verbosity. 0 means no verbosity.

    Returns
    -------
    FabricDataFrame
        :class:`~sempy.fabric.FabricDataFrame` holding the computed measure stratified by groupby columns.
    """  # noqa E501

    # The REST API does not allow for pagination when using the "top" feature. Since the maximum page size is
    # 30,000 rows, we prevent the user from triggering pagination with num_rows set.
    if use_xmla:
        mode = ConnectionMode.XMLA
    else:
        if num_rows and num_rows > 30000:
            if verbose > 0:
                print(f"Provided num_rows ({num_rows}) is greater than 30,000. Switching to XMLA backend.")
            mode = ConnectionMode.XMLA
        else:
            mode = ConnectionMode.REST

    return _get_or_create_workspace_client(workspace) \
        .get_dataset_client(dataset, mode=mode) \
        .evaluate_measure(measure, groupby_columns, filters, fully_qualified_columns, num_rows, verbose)     # type: ignore


@log
def evaluate_dax(
    dataset: Union[str, UUID],
    dax_string: str,
    workspace: Optional[Union[str, UUID]] = None,
    verbose: int = 0
) -> FabricDataFrame:
    """
    Compute `DAX <https://learn.microsoft.com/en-us/dax/>`_ query for a given dataset.

    Parameters
    ----------
    dataset : str or uuid.UUID
        Name or UUID of the dataset.
    dax_string : str
        The DAX query.
    workspace : str or uuid.UUID, default=None
        The Fabric workspace name or UUID object containing the workspace ID.
        Defaults to None which resolves to the workspace of the attached lakehouse
        or if no lakehouse attached, resolves to the workspace of the notebook.
    verbose : int
        Verbosity. 0 means no verbosity.

    Returns
    -------
    FabricDataFrame
        :class:`~sempy.fabric.FabricDataFrame` holding the result of the DAX query.
    """
    client: DatasetXmlaClient = _get_or_create_workspace_client(workspace).get_dataset_client(dataset, mode=ConnectionMode.XMLA)  # type: ignore
    return client.evaluate_dax(dax_string, verbose)


@log
def _trace_evaluate_dax(
    dataset: Union[str, UUID],
    dax_string: str,
    trace_event_schema: Optional[Dict[str, List[str]]] = None,
    start_delay: int = 3,
    stop_timeout: int = 5,
    workspace: Optional[Union[str, UUID]] = None,
    verbose: int = 0
) -> Tuple[FabricDataFrame, pd.DataFrame]:
    """
    Compute `DAX <https://learn.microsoft.com/en-us/dax/>`_ query for a given dataset, with Tracing enabled.

    Parameters
    ----------
    dataset : str or uuid.UUID
        Name or UUID of the dataset to list the measures for.
    dax_string : str
        The DAX query.
    trace_event_schema : dict, default=None
        Dictionary containing Trace event schema to use.
        If None, default events and columns will be used using :meth:`~sempy.fabric.Trace.get_default_query_trace_schema`.
        Note: Using event classes that do not specify SessionID as a column may result in recording events that are not related to this
        specific query execution.
    start_delay : int, delay=3
        Number of seconds to sleep for after starting the trace to allow engine to subscribe to added trace events.
    stop_timeout : int, default=5
        Number of seconds to wait for QueryEnd event to register.
        If QueryEnd is not reached in this time frame, the collected trace logs will still be returned but may be incomplete.
    workspace : str or uuid.UUID, default=None
        The Fabric workspace name or UUID object containing the workspace ID.
        Defaults to None which resolves to the workspace of the attached lakehouse
        or if no lakehouse attached, resolves to the workspace of the notebook.
    verbose : int
        Verbosity. 0 means no verbosity.

    Returns
    -------
    tuple of FabricDataFrame and pd.DataFrame
        Result of the DAX query as a :class:`~sempy.fabric.FabricDataFrame`, and the corresponding trace logs (without the SessionID column).
    """
    client: DatasetXmlaClient = _get_or_create_workspace_client(workspace).get_dataset_client(dataset, mode=ConnectionMode.XMLA)  # type: ignore

    with TraceConnection(client) as trace_connection:
        event_schema = trace_event_schema if trace_event_schema else Trace.get_default_query_trace_schema()
        adomd_session_id = client.get_adomd_connection().get_or_create_connection().SessionID

        with trace_connection.create_trace(event_schema=event_schema, stop_event="QueryEnd") as trace:
            trace.set_filter(lambda e: e.SessionID == adomd_session_id if hasattr(e, "SessionID") else True)
            trace.start(delay=start_delay)
            result = client.evaluate_dax(dax_string, verbose)
            trace_logs = trace.stop(timeout=stop_timeout)

    trace_logs = trace_logs.drop("SessionID", axis=1)
    return result, trace_logs


@log_tables
def plot_relationships(
    tables: Union[Dict[str, FabricDataFrame], List[FabricDataFrame]],
    include_columns='keys',
    missing_key_errors='raise',
    *,
    graph_attributes: Optional[Dict] = None
) -> graphviz.Digraph:
    """
    Visualize relationship dataframe with a graph.

    Parameters
    ----------
    tables : dict[str, sempy.fabric.FabricDataFrame] or list[sempy.fabric.FabricDataFrame]
        A dictionary that maps table names to the dataframes with table content.
        If a list of dataframes is provided, the function will try to infer the names from the
        session variables and if it cannot, it will use the positional index to describe them in
        the results.
        It needs to provided only when `include_columns` = 'all' and it will be used
        for mapping table names from relationships to the dataframe columns.
    include_columns : str, default='keys'
        One of 'keys', 'all', 'none'. Indicates which columns should be included in the graph.
    missing_key_errors : str, default='raise'
        One of 'raise', 'warn', 'ignore'. Action to take when either table or column
        of the relationship is not found in the elements of the argument *tables*.
    graph_attributes : dict, default=None
        Attributes passed to graphviz. Note that all values need to be strings. Useful attributes are:

        - *rankdir*: "TB" (top-bottom) or "LR" (left-right)
        - *dpi*:  "100", "30", etc. (dots per inch)
        - *splines*: "ortho", "compound", "line", "curved", "spline" (line shape)

    Returns
    -------
    graphviz.Digraph
        Graph object containing all relationships.
        If include_attributes is true, attributes are represented as ports in the graph.
    """
    named_dataframes = _to_dataframe_dict(tables)
    relationships = _get_relationships(named_dataframes)
    return plot_relationship_metadata(
        relationships,
        tables,
        include_columns=include_columns,
        missing_key_errors=missing_key_errors,
        graph_attributes=graph_attributes)


@log
def list_relationships(
    dataset: Union[str, UUID],
    workspace: Optional[Union[str, UUID]] = None
) -> pd.DataFrame:
    """
    List all relationship found within the Power BI model.

    Parameters
    ----------
    dataset : str or uuid.UUID
        Name or UUID of the dataset.
    workspace : str or uuid.UUID, default=None
        The Fabric workspace name or UUID object containing the workspace ID. Defaults to None
        which resolves to the workspace of the attached lakehouse
        or if no lakehouse attached, resolves to the workspace of the notebook.

    Returns
    -------
    pandas.DataFrame
        DataFrame with one row per relationship.
    """
    return _get_or_create_workspace_client(workspace).get_dataset_client(dataset, ConnectionMode.XMLA).list_relationships()


@log_tables
def list_relationship_violations(
        tables: Union[Dict[str, FabricDataFrame], List[FabricDataFrame]],
        missing_key_errors='raise',
        coverage_threshold: float = 1.0,
        n_keys: int = 10
) -> pd.DataFrame:
    """
    Validate if the content of tables matches relationships.

    Relationships are extracted from the metadata in FabricDataFrames.
    The function examines results of joins for provided relationships and
    searches for inconsistencies with the specified relationship multiplicity.

    Relationships from empty tables (dataframes) are assumed as valid.

    Parameters
    ----------
    tables : dict[str, sempy.fabric.FabricDataFrame] or list[sempy.fabric.FabricDataFrame]
        A dictionary that maps table names to the dataframes with table content.
        If a list of dataframes is provided, the function will try to infer the names from the
        session variables and if it cannot, it will use the positional index to describe them in
        the results.
    missing_key_errors : str, default='raise'
        One of 'raise', 'warn', 'ignore'. Action to take when either table or column
        of the relationship is not found in the elements of the argument *tables*.
    coverage_threshold : float, default=1.0
        Fraction of rows in the "from" part that need to join in inner join.
    n_keys : int, default=10
        Number of missing keys to report. Random collection can be reported.

    Returns
    -------
    pandas.DataFrame
        Dataframe with relationships, error type and error message.
        If there are no violations, returns an empty DataFrame.
    """
    named_dataframes = _to_dataframe_dict(tables)
    relationships = _get_relationships(named_dataframes)
    return _list_relationship_violations(named_dataframes, relationships, missing_key_errors, coverage_threshold, n_keys)


@log
def resolve_workspace_id(workspace: Optional[Union[str, UUID]] = None) -> str:
    """
    Resolve the workspace name or ID to the workspace UUID.

    Parameters
    ----------
    workspace : str or uuid.UUID, default=None
        The Fabric workspace name or UUID object containing the workspace ID. Defaults to None
        which resolves to the workspace of the attached lakehouse
        or if no lakehouse attached, resolves to the workspace of the notebook.

    Returns
    -------
    uuid.UUID
        The workspace UUID.
    """
    return _get_or_create_workspace_client(workspace).get_workspace_id()


@log
def resolve_workspace_name(workspace: Optional[Union[str, UUID]] = None) -> str:
    """
    Resolve the workspace name or ID to the workspace name.

    Parameters
    ----------
    workspace : str or uuid.UUID, default=None
        The Fabric workspace name or UUID object containing the workspace ID. Defaults to None
        which resolves to the workspace of the attached lakehouse
        or if no lakehouse attached, resolves to the workspace of the notebook.

    Returns
    -------
    str
        The workspace name.
    """
    return _get_or_create_workspace_client(workspace).get_workspace_name()


@log
def create_trace_connection(
    dataset: Union[str, UUID],
    workspace: Optional[Union[str, UUID]] = None
) -> TraceConnection:
    """
    Create a TraceConnection to the server specified by the dataset.

    NOTE: This feature is only intended for exploratory use. Due to the asynchronous communication required between the
    Microsoft Analysis Services (AS) Server and other AS clients, trace events are registered on a best-effort basis where timings are
    dependent on server load.

    Parameters
    ----------
    dataset : str or uuid.UUID
        Name or UUID of the dataset to list traces on.
    workspace : str or uuid.UUID, default=None
        The Fabric workspace name or UUID object containing the workspace ID. Defaults to None
        which resolves to the workspace of the attached lakehouse
        or if no lakehouse attached, resolves to the workspace of the notebook.

    Returns
    -------
    TraceConnection
        Server connected to specified dataset.
    """
    dataset_client: DatasetXmlaClient = _get_or_create_workspace_client(workspace).get_dataset_client(dataset, ConnectionMode.XMLA)   # type: ignore
    return TraceConnection(dataset_client)


@log
def list_workspaces(filter: Optional[str] = None, top: Optional[int] = None, skip: Optional[int] = None) -> pd.DataFrame:
    """
    Return a list of workspaces the user has access to.

    Parameters
    ----------
    filter : str, default=None
        OData filter expression. For example, to filter by name, use "name eq 'My workspace'".
    top : int, default=None
        Maximum number of workspaces to return.
    skip : int, default=None
        Number of workspaces to skip.

    Returns
    -------
    pandas.DataFrame
        DataFrame with one row per workspace.
    """

    rest_api = _PBIRestAPI(token_provider=SynapseTokenProvider())

    payload = rest_api.list_workspaces(filter, top, skip)

    return rename_and_validate_from_records(payload, [
                               ("id", "Id", "str"),
                               ("isReadOnly", "Is Read Only", "bool"),
                               ("isOnDedicatedCapacity", "Is On Dedicated Capacity", "bool"),
                               ("capacityId", "Capacity Id", "str"),
                               ("defaultDatasetStorageFormat", "Default Dataset Storage Format", "str"),
                               ("type", "Type", "str"),
                               ("name", "Name", "str")])


@log
def list_reports(workspace: Optional[Union[str, UUID]] = None) -> pd.DataFrame:
    """
    Return a list of reports in the specified workspace.

    Parameters
    ----------
    workspace : str or uuid.UUID, default=None
        The Fabric workspace name or UUID object containing the workspace ID. Defaults to None
        which resolves to the workspace of the attached lakehouse
        or if no lakehouse attached, resolves to the workspace of the notebook.

    Returns
    -------
    pandas.DataFrame
        DataFrame with one row per report.
    """

    return _get_or_create_workspace_client(workspace).list_reports()
