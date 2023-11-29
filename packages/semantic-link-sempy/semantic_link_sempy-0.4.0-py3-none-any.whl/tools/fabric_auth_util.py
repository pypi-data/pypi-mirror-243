import hashlib
import json
import os
import subprocess

from sempy.fabric._token_provider import _get_token_seconds_remaining, ConstantTokenProvider
from sempy.fabric._client._workspace_client import WorkspaceClient

from tools.trident_utils import env_capacity_id, env_cred, env_endpoint, env_user_id, get_bearer_token, create_workspace

from typing import Optional


class FabricAuthUtil:
    """
    # check if .fabric-token exists
    #    parse and done :)
    #
    # 1. get corpnet user token via "az login --use-device-code" to access keyvault
    # 2. get environment (edog/dxt/msit) username/password from keyvault
    # 3. get bearer token for environment username/password
    # 4. create workspace (re-use if exists)
    # 5. store the token in .fabric-token
    """
    env_bearer_token: Optional[str] = None

    user_keyvaults = {
        "edog": {
           "vault": "PBITenantAdminAccounts",
           "secret-name": "admin-EnvRunnersTestUsersSecret-pbiedog"
        },
        "daily": {
           "vault": "PBITenantAdminAccounts",
           "secret-name": "admin-EnvRunnersTestUsersSecret-pbidaily"
        },
        "dxt": {
            "vault": "PBITenantAdminAccounts",
            "secret-name": "admin-EnvRunnersTestUsersSecret-pbidxt"
        },
        "msit": {
            "vault": "PBITenantAdminAccounts",
            "secret-name": "admin-EnvRunnersTestUsersSecret-pbimsit"
        },
    }

    def __init__(self, env: str):
        self.env = env

    @staticmethod
    def get_dev_user():
        """Returns the developer's username."""

        # alternative is to fetch from environment, doesn't work well w/ devcontainer
        # return environ["USERNAME"] if platform.startswith("win") else environ["USER"]

        git_email = subprocess.getoutput("git config user.email")
        # extract username from email
        if "@" in git_email:
            return git_email.split("@")[0]
        else:
            return "PR"

    def get_env_username(self) -> str:
        """Returns the username for the environment (edog/dxt/msit)."""
        return env_cred[self.env]

    def get_env_password(self):
        # check environment first
        env_password = os.environ.get("ut_password")
        if env_password is not None:
            return env_password

        # use AZ cli to fetch username/password from keyvault
        from azure.keyvault.secrets import SecretClient
        from azure.identity import AzureCliCredential

        try:
            # fetch username/password from keyvault using AZ cli credentials
            vault_name = self.user_keyvaults[self.env]["vault"]
            key_vault_uri = f"https://{vault_name}.vault.azure.net"

            credential = AzureCliCredential()
            client = SecretClient(vault_url=key_vault_uri, credential=credential)
            retrieved_secret = client.get_secret(self.user_keyvaults[self.env]["secret-name"])

            return retrieved_secret.value
        except Exception as e:
            raise ValueError(f"""
    Unable to retrieve secret. Try

    az login
    az account set --subscription e342c2c0-f844-4b18-9208-52c8c234c30e

    Error: {e}""")

    def get_env_bearer_token(self) -> str:
        """Returns the bearer token for the environment (edog/dxt/msit)."""

        # useful to test using a specific token
        # import base64
        # token = ""
        # bearer_token_fabric = base64.b64decode(token.encode('ascii')).decode('ascii')
        # return bearer_token_fabric

        if self.env_bearer_token is not None:
            return self.env_bearer_token

        username = self.get_env_username()
        password = self.get_env_password()

        # useful to retrieve username/password to interactively explore your workspace
        print(f"USERNAME: {username} PASSWORD: {hashlib.md5(password.encode('utf-8')).hexdigest()}")

        self.env_bearer_token = get_bearer_token(self.env, username, password)

        return self.env_bearer_token

    def _get_or_create_workspace(self, workspace_name: str):
        token_provider = ConstantTokenProvider(self.get_env_bearer_token())
        workspace_id = WorkspaceClient(workspace_name, token_provider).get_workspace_id()

        if workspace_id is None:
            workspace_id = create_workspace(env_endpoint[self.env],
                                            self.get_env_bearer_token(),
                                            self.get_env_username(),
                                            env_capacity_id[self.env],
                                            env_user_id[self.env],
                                            workspace_name)

        return workspace_id

    def get_fabric_config(self) -> dict[str, str]:
        workspace_name = f"SemPy {FabricAuthUtil.get_dev_user()}"
        cache_path = ".fabric-config"

        if os.path.exists(cache_path):
            fabric_config = json.loads(open(cache_path, "r").read())

            # check if token is still valid and if the workspace/identity matches
            # in case user was switching between environments/identities:
            if (
                _get_token_seconds_remaining(fabric_config["bearer_token"]) > 60 and
                fabric_config.get("workspace_name", None) == workspace_name and
                fabric_config.get("identity", None) == env_user_id[self.env]
            ):
                return fabric_config

        workspace_id = self._get_or_create_workspace(workspace_name)

        bearer_token_fabric = self.get_env_bearer_token()

        fabric_config = {
            "bearer_token": bearer_token_fabric,
            "workspace_id": workspace_id,
            "workspace_name": workspace_name,
            "identity": env_user_id[self.env]
        }

        # cache the token
        with open(cache_path, "w") as f:
            f.write(json.dumps(fabric_config, default=str))

        return fabric_config
