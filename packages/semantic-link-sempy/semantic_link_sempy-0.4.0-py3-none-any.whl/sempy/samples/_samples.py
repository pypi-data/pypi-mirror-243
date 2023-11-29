import numpy as np
import os
import pandas as pd
from urllib.request import urlretrieve
from zipfile import ZipFile

from sempy.fabric._client._tools import upload_to_lakehouse
from sempy.fabric._environment import _get_onelake_endpoint, _on_fabric, get_workspace_id, get_lakehouse_id

from typing import Optional


def download_synthea(which: str = 'small', workspace_id: Optional[str] = None, lakehouse_id: Optional[str] = None) -> str:
    """
    Download and cache synthea example datasets for demos.

    See https://synthea.mitre.org/downloads for a description.

    Parameters
    ----------
    which : str, default='small'
        Dataset selector, see url above for details. Can be 'small' or 'covid'.

    workspace_id : str, default=None
        Required when running on Fabric.

    lakehouse_id : str, default=None
        Required when running on Fabric.

    Returns
    -------
    str
        Path to CSV files.
    """
    if which == "small":
        result_path = "synthea/csv"
        url = "https://synthetichealth.github.io/synthea-sample-data/downloads/synthea_sample_data_csv_apr2020.zip"
    elif which == "covid":
        result_path = "synthea/10k_synthea_covid19_csv"
        url = "https://synthetichealth.github.io/synthea-sample-data/downloads/10k_synthea_covid19_csv.zip"
    else:
        raise ValueError(f"Unknown argument which='{which}'")
    if not os.path.exists(result_path):
        file, reply = urlretrieve(url)
        zfile = ZipFile(file)
        zfile.extractall(path="synthea/")

    if _on_fabric():
        from trident_token_library_wrapper import PyTridentTokenLibrary
        bearer_token = PyTridentTokenLibrary.get_access_token("storage")

        if workspace_id is None:
            workspace_id = get_workspace_id()
        if lakehouse_id is None:
            lakehouse_id = get_lakehouse_id()

        onelake = _get_onelake_endpoint()
        upload_to_lakehouse("synthea", workspace_id, lakehouse_id, onelake, bearer_token)
        result_path = f"abfss://{workspace_id}@{onelake}/{lakehouse_id}/Files/{result_path}"

    return result_path


def _make_time_data(n_time_periods: int = 500, n_groups: int = 4, freq: str = 'D') -> pd.DataFrame:
    """
    Make random grouped time data.

    This creates 2 * n_groups many Brownian motion time series with regular observation frequency given by "D".
    The data is returned with n_groups in long format, with one column indicating the group, and two amounts per group in wide format.
    This means the resulting SemanticDataFrame has four attributes, date, amount, other_amount and group.

    In essence this generates a data-cube of n_groups x 2 x n_time_periods, with the first dimension represented in long format.

    This is supposed to simulate data with two independent groupings, say having patients (the groups),
    and for each patient weight (amount) and blood sugar (other_amount) over time.
    Or having warehouses (groups) and demand and supply over time; or the demand for different products over time.

    Parameters
    ----------
    n_time_periods : int, default=500
        Number of time stamps / periods in data.
    n_groups : int, default=4
        Number of groups in data.
    freq : str, default='D'
        Frequency / time step in time index.

    Returns
    -------
    DataFrame
        Synthetic dataset.
    """
    # Create several Brownian motion series.
    data = np.cumsum(np.random.normal(size=(n_time_periods, n_groups)), axis=0) + np.random.normal(10, 10, size=(1, n_groups))
    # Make into wide form time series.
    date_index = pd.date_range(start="01/02/2003", freq=freq, periods=n_time_periods)
    df = pd.DataFrame(data, index=date_index, columns=[f"group_{i}" for i in range(n_groups)])
    # make into long form with group variable expanded.
    long_format = df.reset_index().melt(id_vars="index", value_name="amount", var_name="group")
    long_format['other_column'] = np.cumsum(np.random.normal(size=(len(long_format))))
    long_format = long_format.rename(columns={'index': 'date'})
    return long_format
