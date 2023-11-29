import datetime
import pandas as pd
import warnings
import re
from dataclasses import dataclass


from pandas.core.dtypes.common import is_dtype_equal
from typing import List, Optional, Tuple


def _pandas_merge_cast(left_df, left_on, right_df, right_on, relationship=None, warn=True):

    if not isinstance(left_on, str) or not isinstance(right_on, str):
        raise TypeError(f"Unexpected types {type(left_on)} and {type(right_on)}: not strings")

    string_types = ["string", "unicode", "mixed", "bytes", "empty"]

    # Try to cast some common type issues to make pandas behave more nicely
    if not is_dtype_equal(left_df[left_on], right_df[right_on]):
        left_dtype = pd.api.types.infer_dtype(left_df[left_on])
        right_dtype = pd.api.types.infer_dtype(right_df[right_on])
        msg = f"Mismatching dtypes in merging along relationship {relationship}."
        if (left_dtype in string_types):
            if (right_dtype in string_types):
                # both are string
                pass
            else:
                # left is string but right is not
                if warn:
                    warnings.warn(msg)
                right_df = right_df.astype({right_on: str})

        elif right_dtype in string_types:
            # right is string but left is not
            if warn:
                warnings.warn(msg)
            left_df = left_df.astype({left_on: str})

    return left_df, right_df


@dataclass
class _Column:
    src: str
    dest: str
    type: str
    optional: bool


_safe_datetime_regex = re.compile(r"""^             # start of string
                                      (\d{4})-      # year
                                      (\d{2})-      # month
                                      (\d{2})T      # day
                                      (\d{2}):      # hour
                                      (\d{2}):      # minute
                                      (\d{2})       # second
                                      (?:\.(\d+))?  # optional milliseconds or nanoseconds
                                      Z?            # optional Z indicating UTC timezone (no support for offset)
                                      $             # end of string
                                  """,
                                  re.VERBOSE)


def safe_convert_rest_datetime(val: Optional[str]):
    if val is None:
        return None

    m = _safe_datetime_regex.match(val)
    if m is None:
        raise ValueError(f"Unable to parse datetime string: {val}")

    (year, month, day, hour, minute, second, ms_or_ns) = m.groups()

    # python doesn't support nanoseconds, just truncate to microseconds
    if ms_or_ns is None:
        ms_or_ns = "0"

    ms_or_ns = ms_or_ns[:6]
    ms_or_ns = "{v:0<6}".format(v=ms_or_ns)

    dt = datetime.datetime(
        year=int(year),
        month=int(month),
        day=int(day),
        hour=int(hour),
        minute=int(minute),
        second=int(second),
        microsecond=int(ms_or_ns),
        tzinfo=datetime.timezone.utc)

    return dt


def _parse_schema(schema: List[Tuple[str, str, str]]) -> List[_Column]:
    # Supported format: <type>[?], where ? indicates optional.
    cols = []
    for src, dest, column_type in schema:
        if column_type.endswith("?"):
            column_type = column_type[:-1]
            optional = True
        else:
            optional = False

        cols.append(_Column(src, dest, column_type, optional))

    return cols


def _check_missing_cols(df: pd.DataFrame, schema: List[_Column]):
    missing_columns = [
        col.src
        for col in schema
        # it's (missing) and (mandatory)
        if col.src not in df.columns.values and not col.optional
    ]

    if len(missing_columns) > 0:
        # don't fail, just warn. Assuming the backend returns less data than expected, we should still
        # pass the data
        warnings.warn(UserWarning(f"Missing columns from backend: {missing_columns}"))


def _insert_missing_cols(df: pd.DataFrame, schema: List[_Column]):
    for col in schema:
        if col.src not in df.columns.values:
            # add missing column as the it's optional in the input data
            df[col.src] = pd.Series(dtype=col.type)


def _convert_columns(df: pd.DataFrame, schema: List[_Column]):
    for col in schema:
        if col.src in df.columns.values and col.type == "datetime64[ns]":
            df[col.src] = df[col.src].apply(safe_convert_rest_datetime)


def rename_and_validate(df: pd.DataFrame, schema: List[Tuple[str, str, str]]) -> pd.DataFrame:
    """
    Rename columns in a dataframe according to a schema and validate that the schema is satisfied.

    Parameters
    ----------
    df : pd.DataFrame
        The input data.
    schema : List[Tuple[str, str, str]]
        The expected schema. Each element is a tuple of (source column name, destination column name, column type).

    Returns
    -------
    pd.DataFrame
        The renamed dataframe.
    """
    schema_cols = _parse_schema(schema)

    # make sure empty dataframes still have the schema and the proper types
    if df is None or len(df) == 0:
        return pd.DataFrame({
            col.dest: pd.Series(dtype=col.type)
            for col in schema_cols
        })

    _check_missing_cols(df, schema_cols)

    # need to convert before inserting as we don't want to deal
    # w/ pd.NaT when trying to convert, rather just str
    _convert_columns(df, schema_cols)

    _insert_missing_cols(df, schema_cols)

    # create new dataframe with renamed columns in the right order (e.g. optional columns would be at the end)
    return pd.DataFrame({col.dest: df[col.src] for col in schema_cols})


def rename_and_validate_from_records(records, schema: List[Tuple[str, str, str]]) -> pd.DataFrame:
    """
    Rename columns in a list of records according to a schema and validate that the schema is satisfied.

    Parameters
    ----------
    records : List[dict]
        The input data.
    schema : List[Tuple[str, str, str]]
        The expected schema. Each element is a tuple of (source column name, destination column name, column type).

    Returns
    -------
    pd.DataFrame
        The renamed dataframe.
    """

    # prep schema
    if records is None or len(records) == 0:
        df = None
    else:
        df = pd.DataFrame.from_records(records)

    return rename_and_validate(df, schema)
