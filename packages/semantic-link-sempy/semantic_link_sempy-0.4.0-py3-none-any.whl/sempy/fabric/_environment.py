import os
from typing import Optional, Any
from urllib.parse import quote

fs_client: Optional[Any] = None
environment: Optional[str] = None

# FIXME: we need a proper API to get base URL from spark config, which currently doesn't seem to exist
# the current hack aligns with https://dev.azure.com/powerbi/Embedded/_git/BugbashTool?path=/PowerBIEmbedded/PowerBIEmbedded/App.config&_a=contents&version=GBmaster
# sovereign clouds are skipped for now.
SUPPORTED_ENVIRONMENTS = {
                'onebox': "onebox-redirect.analysis.windows-int.net/",
                'daily': "dailyapi.powerbi.com/",
                'edog': "powerbiapi.analysis-df.windows.net/",
                'dxt': "powerbistagingapi.analysis.windows.net/",
                'msit': "df-msit-scus-redirect.analysis.windows.net/",
                'prod': "api.powerbi.com/",
        }

# https://dev.azure.com/powerbi/Trident/_wiki/wikis/Trident.wiki/46148/Environments
SUPPORTED_FABRIC_REST_ENVIRONMENTS = {
                'onebox': "analysis.windows-int.net/powerbi/api/",
                'daily': "analysis.windows-int.net/powerbi/api/",
                'edog': "api.fabric.microsoft.com/",
                'dxt': "api.fabric.microsoft.com/",
                'msit': "api.fabric.microsoft.com/",
                'prod': "api.fabric.microsoft.com/",
}


def get_workspace_id() -> str:
    """
    Return workspace id.

    Returns
    -------
    str
        Workspace id guid.
    """
    return _get_trident_config('trident.workspace.id')


def get_lakehouse_id() -> str:
    """
    Return lakehouse id of the lakehouse that is connected to the workspace.

    Returns
    -------
    str
        Lakehouse id guid.
    """
    return _get_trident_config('trident.lakehouse.id')


def get_notebook_workspace_id() -> str:
    """
    Return notebook workspace id.

    Returns
    -------
    str
        Workspace id guid.
    """
    return _get_trident_config('trident.artifact.workspace.id')


def get_artifact_id() -> str:
    """
    Return artifact id.

    Returns
    -------
    str
        Artifact (most commonly notebook) id guid.
    """
    return _get_trident_config('trident.artifact.id')


def _get_artifact_type() -> str:
    """
    Return artifact type.

    Returns
    -------
    str
        Artifact type e.g. "SynapseNotebook".
    """
    return _get_trident_config('trident.artifact.type')


def _get_onelake_endpoint() -> str:
    """
    Return onelake endpoint for the lakehouse.

    Returns
    -------
    str
        Onelake endpoint.
    """
    endpoint = _get_trident_config("trident.onelake.endpoint")
    return endpoint.split('/')[2]


def _get_trident_config(key: str) -> str:
    if _on_fabric():
        from pyspark import SparkContext
        sc = SparkContext.getOrCreate()
        value = sc._jsc.hadoopConfiguration().get(key)
        assert isinstance(value, str)
        return value
    else:
        return "local"


def _get_synapse_endpoint() -> str:
    return f"https://{SUPPORTED_ENVIRONMENTS[_get_environment()]}"


def _get_pbi_uri() -> str:
    return f"powerbi://{SUPPORTED_ENVIRONMENTS[_get_environment()]}"


def _get_fabric_rest_endpoint() -> str:
    return f"https://{SUPPORTED_FABRIC_REST_ENVIRONMENTS[_get_environment()]}"


def _get_workspace_url(workspace: str) -> str:
    url = f"{_get_pbi_uri()}v1.0/myorg/"
    if workspace == "My workspace":
        return url
    else:
        return f"{url}{quote(workspace)}"


def _get_workspace_path(workspace_name: str, workspace_id: str):
    if workspace_name == "My workspace":
        # retrieving datasets from "My workspace" (does not have a group GUID) requires a different query
        return "v1.0/myorg/"
    else:
        return f"v1.0/myorg/groups/{workspace_id}/"


def _get_environment() -> str:

    global environment

    if environment is None:

        if _on_fabric():
            from pyspark.sql import SparkSession
            sc = SparkSession.builder.getOrCreate().sparkContext
            environment = sc.getConf().get("spark.trident.pbienv")

        if environment is None:
            environment = 'msit'

        environment = environment.lower().strip()

        if environment not in SUPPORTED_ENVIRONMENTS:
            raise ValueError(f"Unsupported environment '{environment}'. We support {list(SUPPORTED_ENVIRONMENTS.keys())}")

    return environment


def _on_fabric() -> bool:
    return 'AZURE_SERVICE' in os.environ
