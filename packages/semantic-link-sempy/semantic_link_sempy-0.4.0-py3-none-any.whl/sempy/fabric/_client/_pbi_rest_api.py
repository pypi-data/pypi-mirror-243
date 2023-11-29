import json
import datetime
import time

from sempy.fabric.exceptions import FabricHTTPException, DatasetNotFoundException, WorkspaceNotFoundException
from sempy.fabric._utils import is_valid_uuid
from sempy.fabric._client._rest_client import PowerBIRestClient
from sempy.fabric._environment import _get_workspace_path
from sempy.fabric._token_provider import TokenProvider
from sempy._utils._log import log
from urllib.parse import quote

from typing import Any, Optional, List, Tuple, Dict


class _PBIRestAPI():
    _rest_client: PowerBIRestClient

    def __init__(self, token_provider: Optional[TokenProvider] = None):
        self._rest_client = PowerBIRestClient(token_provider)

    def list_workspaces(self, filter: Optional[str] = None, top: Optional[int] = None, skip: Optional[int] = None):
        params = []

        path = "v1.0/myorg/groups"
        if filter is not None:
            params.append(f"$filter={filter}")
        if top is not None:
            params.append(f"$top={top}")
        if skip is not None:
            params.append(f"$skip={skip}")

        if len(params) > 0:
            path += "?" + "&".join(params)

        response = self._rest_client.get(path)

        value = response.json()['value']
        if len(value) == 0:
            return None
        else:
            return value

    def get_workspace_name_from_id(self, workspace_id: str) -> str:
        # We got shot in the foot by an empty string, which retrieves all workspaces
        # and results in unexpected format of the response, so validate:
        if not is_valid_uuid(workspace_id):
            raise ValueError(f"Invalid UUID '{workspace_id}' in \"workspace_id\"")

        try:
            response = self._rest_client.get(f"v1.0/myorg/groups/{workspace_id}")
            return response.json()['name']
        except FabricHTTPException as e:
            if e.status_code == 401:
                if "Calling group APIs not permitted for personal workspace" in e.error_text:
                    return "My workspace"
                else:
                    # If the GUID is does not exist, PBI REST returns "Unauthorized", which goes
                    # against more common practice of 404 "Not found". It's debatable which
                    # way we should be aligning.
                    raise WorkspaceNotFoundException(workspace_id)
            else:
                raise

    def get_workspace_datasets(self, workspace_name: str, workspace_id: str):
        path = _get_workspace_path(workspace_name, workspace_id) + "datasets"
        res = self._rest_client.get(path)
        return res.json()["value"]

    @staticmethod
    def create_refresh_body(
        refresh_type,
        max_parallelism,
        commit_mode,
        retry_count,
        apply_refresh_policy,
        effective_date,
        objects: Optional[List] = None
    ) -> dict:
        # validating values in 'objects' argument
        if objects is not None:
            for table in objects:
                if not isinstance(table, dict):
                    raise ValueError("Each element in the 'objects' list must be a dictionary.")
                if "table" not in table:
                    raise ValueError("Each dictionary in the 'objects' list must include a 'table' key.")
                elif not isinstance(table["table"], str):
                    raise ValueError("The 'table' value in each dictionary (if present) must be a string.")
                if "partition" in table and not isinstance(table["partition"], str):
                    raise ValueError("The 'partition' value in each dictionary (if present) must be a string.")

        # preprocessing of date value
        date_str = effective_date.strftime("%Y-%m-%dT%H:%M:%S")
        data_structure = {
            "type": refresh_type,
            "commitMode": commit_mode,
            "maxParallelism": max_parallelism,
            "retryCount": retry_count,
            "applyRefreshPolicy": apply_refresh_policy,
            "effectiveDate": date_str,
            "objects": objects
        }
        return data_structure

    def refresh_post(
            self,
            dataset_id: str,
            workspace_id: str,
            workspace_name: str,
            refresh_type: str = "automatic",
            max_parallelism: int = 10,
            commit_mode: str = "transactional",
            retry_count: int = 0,
            objects: Optional[List] = None,
            apply_refresh_policy: bool = True,
            effective_date: datetime.date = datetime.date.today(),
            verbose: int = 0
    ) -> str:

        path = _get_workspace_path(workspace_name, workspace_id)
        path += f"datasets/{dataset_id}/refreshes"
        body = _PBIRestAPI.create_refresh_body(refresh_type, max_parallelism, commit_mode, retry_count,
                                               apply_refresh_policy, effective_date, objects)
        json_dumps_params = json.dumps(body)
        response = self._rest_client.post(path, data=json_dumps_params, headers={'Content-Type': 'application/json'})
        poll_url = None
        if getattr(response, 'headers', None) is not None:
            poll_url = response.headers.get('Location')
            request_id = response.headers.get('RequestId')
            if verbose:
                print(f"request id: {request_id}")

        if poll_url is None:
            raise ValueError("Poll URL not found in the response.")
        return poll_url

    def get_refresh_execution_details(
            self,
            dataset_id: str,
            request_id: str,
            workspace_id: str,
            workspace_name: str
            ) -> dict:
        # https://learn.microsoft.com/en-us/rest/api/power-bi/datasets/get-refresh-execution-details#datasetrefreshdetail

        path = _get_workspace_path(workspace_name, workspace_id)
        path += f"datasets/{dataset_id}/refreshes/{request_id}"

        response = self._rest_client.get(path)
        if response.status_code not in [200, 202]:
            raise ValueError(f"Failed to retrieve refresh status for {dataset_id}. Response code: {response.status_code} {response.text}")

        return response.json()

    def list_refresh_history(
            self,
            dataset_id: str,
            workspace_id: str,
            workspace_name: str,
            top_n: Optional[int] = None
    ) -> dict:
        # https://learn.microsoft.com/en-us/rest/api/power-bi/datasets/get-refresh-history

        path = _get_workspace_path(workspace_name, workspace_id)
        path += f"/datasets/{dataset_id}/refreshes"

        if top_n is not None:
            path = path + f"?$top={top_n}"

        response = self._rest_client.get(path)
        if response.status_code not in [200, 202]:
            raise ValueError(f"Failed to retrieve refresh status for {dataset_id}. Response code: {response.status_code} {response.text}")

        return response.json()["value"]

    def get_dataset_name_from_id(self, dataset_id: str, workspace_name: str) -> str:
        try:
            res = self._rest_client.get(f"v1.0/myorg/datasets/{dataset_id}")
        except FabricHTTPException as e:
            if e.status_code == 404:
                raise DatasetNotFoundException(dataset_id, workspace_name)
            else:
                raise
        return res.json()["name"]

    def get_dataset_model_id(self, dataset_id: str):
        path = f"metadata/gallery/SharedDatasets/{dataset_id}"
        res = self._rest_client.get(path)
        return res.json()['modelId']

    def get_dataset_schema_entitites(self, dataset_id: str):
        dataset_model_id = self.get_dataset_model_id(dataset_id)
        payload = {
            "modelIds": [dataset_model_id],
            "userPreferredLocale": "en-US"
        }
        res = self._rest_client.post("explore/conceptualschema", json=payload)
        return res.json()["schemas"][0]["schema"]["Entities"]

    def execute_dax_query(self, dataset_id: str, query: str):
        path = f"v1.0/myorg/datasets/{dataset_id}/executeQueries"
        payload = {
            "queries": [{
                "query": f"{query}"
            }]
        }
        res = self._rest_client.post(path, json=payload)
        return res.json()["results"][0]["tables"][0]["rows"]

    def calculate_measure(
        self,
        dataset_id: str,
        measure: List[Dict[str, str]],
        groupby_columns: List[Dict[str, str]],
        filters: List[Dict[str, list]],
        num_rows: Optional[int],
        verbose: int
    ) -> Tuple[List[dict], List[list]]:

        # The REST API returns empty results as an error saying "Query evaluation produced no result".
        # We want to return an empty dataframe in this case to match XMLA output.
        # TODO: PBI team should not be throwing an error for empty results (flagging for follow-up)
        try:
            res = self._retrieve_measure(dataset_id, measure, groupby_columns, filters, num_rows, verbose)
        except FabricHTTPException as e:
            if "Query evaluation produced no result" in e.error_text:
                return [], []
            else:
                raise e

        rows = res["rows"]
        columns = res["columns"]

        while "continuationToken" in res:
            cont_token = res["continuationToken"]
            res = self._retrieve_measure(dataset_id, measure, groupby_columns, filters, num_rows, verbose, cont_token=cont_token)
            rows.extend(res["rows"])

        return columns, rows

    def _retrieve_measure(
        self,
        dataset_id: str,
        measure_obj: List[Dict[str, str]],
        groupby_columns_obj: List[Dict[str, str]],
        filter_obj: List[Dict[str, list]],
        num_rows: Optional[int],
        verbose: int,
        cont_token: str = ""
    ):
        path = "v1.0/myOrg/internalMetrics/query"
        payload = {
            "provider": {
                "datasetId": dataset_id
            },
            "metrics": measure_obj,
            "groupBy": groupby_columns_obj,
            "filters": filter_obj,
            "paginationSettings": {
                "continuationToken": cont_token
            },
            "top": num_rows
        }

        if verbose > 0:
            print(f"Executing REST query with payload: {json.dumps(payload, indent=2)}")
        res = self._rest_client.post(path, json=payload, headers={"App-Name": "SemPy"})
        return res.json()

    @log
    def upload_pbix(self, dataset_name: str, pbix: bytes, workspace_id: str, workspace_name: str, skip_report: bool = True):
        path = _get_workspace_path(workspace_name, workspace_id)

        path = f"{path}/imports?datasetDisplayName={quote(dataset_name)}"
        path += f"&nameConflict=CreateOrOverwrite&skipReport={skip_report}&overrideReportLabel=true&overrideModelLabel=true"

        payload: Any = {}
        files = [('', (dataset_name, pbix, 'application/octet-stream'))]

        response = self._rest_client.post(path, data=payload, files=files)

        if response.status_code != 202:
            raise Exception(f"Importing of '{dataset_name}' not accepted. Response code: {response.status_code}")

        attempts = 0
        sleep_factor = 1.5
        while attempts < 10:
            response = self._rest_client.get(path, data=payload, files=files)
            if response.status_code == 200:
                time.sleep(30)
                break
            time.sleep(sleep_factor ** attempts)
            attempts += 1

        if attempts == 10:
            raise TimeoutError("Dataset upload to workspace timed out.")

    def update_dataset_storage_mode(self, dataset_id: str, target_storage_mode: int):
        # update
        url = self._rest_client.base_url + f"v1.0/myorg/datasets/{dataset_id}"

        response = self._rest_client.patch(url, json={"targetStorageMode": target_storage_mode})

        if response.status_code != 200:
            raise Exception(f"Failed to update targetStorageMode for {dataset_id}. Response code: {response.status_code}")

        # wait for update to finish
        model_id = self.get_dataset_model_id(dataset_id)
        url = self._rest_client.base_url + f"metadata/models/{model_id}/storageModeConversionStatus"

        attempts = 0
        while attempts < 10:
            # {"storageMode":2,"conversionStatus":1}
            response = self._rest_client.get(url)

            if response.status_code == 200 and response.json()["conversionStatus"] == 1:
                return

            time.sleep(2)
            attempts += 1

        raise TimeoutError("Updating targetStorageMode timed out.")

    def update_dataset_export_to_onelake(self, dataset_id: str, export: bool = True):
        model_id = self.get_dataset_model_id(dataset_id)

        url = self._rest_client.base_url + f"metadata/models/{model_id}/settings"
        payload = {
            "exportToOneLake": export
        }

        response = self._rest_client.post(url, json=payload)

        if response.status_code != 204:
            raise Exception(f"Failed to update exportToOneLake for {dataset_id}. Response code: {response.status_code}")

    def list_reports(self, workspace_name: str, workspace_id: str):
        path = _get_workspace_path(workspace_name, workspace_id) + "reports"
        res = self._rest_client.get(path)

        if res.status_code != 200:
            raise ValueError(f"Failed to retrieve reports from workspace '{workspace_id}': {res.status_code}")

        return res.json()["value"]
