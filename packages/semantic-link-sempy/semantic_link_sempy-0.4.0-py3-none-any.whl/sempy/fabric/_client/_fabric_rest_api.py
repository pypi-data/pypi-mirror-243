from sempy.fabric._client._rest_client import FabricRestClient
from sempy.fabric.exceptions import WorkspaceNotFoundException
from sempy.fabric._token_provider import TokenProvider

from typing import Optional


class _FabricRestAPI():
    _rest_client: FabricRestClient

    def __init__(self, token_provider: Optional[TokenProvider] = None):
        self._rest_client = FabricRestClient(token_provider)

    def get_my_workspace_id(self) -> str:
        # TODO: we should align on a single API to retrieve workspaces using a single API,
        #       but we need to wait until the API support filtering and paging
        # Using new Fabric REST endpoints
        response = self._rest_client.get("v1/workspaces")

        if response.status_code != 200:
            raise WorkspaceNotFoundException("My workspace")

        payload = response.json()["value"]

        workspaces = [ws for ws in payload if ws["type"] == 'Personal']

        if len(workspaces) != 1:
            raise ValueError(f"Unable to resolve My workspace ID. Zero or more than one workspaces found ({len(workspaces)})")

        return workspaces[0]['id']
