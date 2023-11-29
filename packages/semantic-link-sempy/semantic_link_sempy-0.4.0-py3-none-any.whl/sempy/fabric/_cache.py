from uuid import UUID

from sempy.fabric._client import WorkspaceClient
from typing import Dict, Optional, Union


_workspace_clients: Dict[Optional[Union[str, UUID]], WorkspaceClient] = dict()


def _get_or_create_workspace_client(workspace_name: Optional[Union[str, UUID]]) -> WorkspaceClient:
    global _workspace_clients

    client = _workspace_clients.get(workspace_name)
    if client is None:
        client = WorkspaceClient(workspace_name)
        _workspace_clients[workspace_name] = client

    return client
