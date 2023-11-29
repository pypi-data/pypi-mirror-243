from urllib.parse import quote
from uuid import uuid4

import json
import requests

CI_NAMED_WORKSPACE_NAME = "(DONT DELETE) SemPy Fabric"

env_cred = {
    "edog": "AzTest@TridentCSTEdog.ccsctp.net",
    "daily": "AdminUser@TridentCSTDaily.onmicrosoft.com",
    "dxt": "AdminUser@TridentCSTDXT.onmicrosoft.com",
    "msit": "AdminUser@TridentCSTMSIT.onmicrosoft.com",
    "prod": "AdminUser@TridentCSTProdWestUS3.onmicrosoft.com",
}

env_endpoint = {
    "edog": "biazure-int-edog-redirect.analysis-df.windows.net",
    "daily": "wabi-daily-us-east2-redirect.analysis.windows.net",
    "dxt": "wabi-staging-us-east-redirect.analysis.windows.net",
    "msit": "df-msit-scus-redirect.analysis.windows.net",
    "prod": "wabi-west-us3-a-primary-redirect.analysis.windows.net",
}

env_capacity_id = {
    "edog": "B9040312-3894-400D-9051-D6107A1994D7",
    "daily": "CC03C367-FF3C-47BC-99C7-5356B14FAEA3",
    "dxt": "C367C00F-C102-4847-8A32-9663E07E03E6",
    "msit": "C488C5CC-681D-4453-A953-F967FA17A5D3",
    "prod": "DD39D0B5-1583-4F1C-9C4B-A2A2B56E1432",
}

env_user_id = {
    "edog": "b9c26e50-6ae0-409f-b4b8-1a4dc41fdb74",
    "daily": "3cf83ccc-40b7-418a-b807-1c02bbbb0a9f",
    "dxt": "c5390f94-f4e3-452c-880d-54c4bf96e2f3",
    "msit": "dc5922b4-acb2-4bdb-9cf7-9a139035b04d"
}

env_onelake = {
    "edog": "onelakeedog.pbidedicated.windows-int.net",
    "daily": "daily-onelake.pbidedicated.windows.net",
    "dxt": "dxt-onelake.pbidedicated.windows.net",
    "msit": "msit-onelake.pbidedicated.windows.net",
    "prod": "onelake.pbidedicated.windows.net",
}

env_onelake_new = {
    "edog": "onelake-int-edog.dfs.pbidedicated.windows-int.net",
    "daily": "daily-onelake.dfs.fabric.microsoft.com",
    "dxt": "dxt-onelake.dfs.fabric.microsoft.com",
    "msit": "msit-onelake.dfs.fabric.microsoft.com",
    "prod": "onelake.dfs.fabric.microsoft.com"
}

env_named_workspace_id = {
    "edog": "d2f3f034-edd3-4040-a559-2bcc93f1bb68",
    "daily": "17453554-6060-47ce-9334-db34450ca211",
    "dxt": "56df6b2e-37fd-40de-86a8-9e1a97e27724",
    "msit": "180ef180-92c9-4a80-b270-ac80aa180553",
    "prod": "e49568dc-d3c8-428f-8458-e6811dd63a5f",
}

env_my_workspace_id = {
    "edog": "db69ce44-6535-4f4f-8d49-13fa90739850",
    "daily": "bca94b5d-ad34-470d-8fe4-7bc7b2a9c0a6",
    "dxt": "7b28b05e-d702-4308-8bfa-224c6108f54c",
    "msit": "97c74ef7-affb-4725-9003-607cb955fd8a",
    "prod": "fc6a1d8b-dbe7-471a-a8b7-b31cb7fb87f9",
}

env_ci_lakehouse_id = {
    "edog": "1328a843-717b-4e06-b86c-620cdb767d32",
    "daily": "06926901-f863-4800-b924-1b80e7298f83",
    "dxt": "f776fa23-5bde-4655-a1ec-7f8545884036",
    "msit": "e8080508-fcba-4c3c-9945-3b0e3fa9acd9",
    "prod": "cfe7103d-9600-43e3-aaaf-ad0874e5e7c2"
}


class AADCredential:
    def __init__(self, token, **kwargs):
        self.token = token

    def get_token(self, *scopes, **kwargs):
        return self.token


def get_bearer_token(env, username, password, audience="pbi"):
    if audience != "pbi" and audience != "storage":
        raise ValueError("Only pbi and storage audiences are supported.")

    # XMLA client id
    client_id = "cf710c6e-dfcc-4fa8-a093-d47294e44c66"
    user, tenant = username.split('@')

    if env == 'edog':
        resource = "https://analysis.windows-int.net/powerbi/api"
        authority = "login.windows-ppe.net"
    else:
        resource = "https://analysis.windows.net/powerbi/api" if audience == "pbi" else "https://storage.azure.com"
        authority = "login.windows.net"

    login_url = f"https://{authority}/{tenant}/oauth2/token"
    payload = f'resource={quote(resource, safe="")}&client_id={client_id}&grant_type=password&username={username}&password={quote(password, safe="")}&scope=openid'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'fpc=AlqdPsBZ3IhEkuEX2q3BHxjyrCATAQAAAAFta9sOAAAALbyONgEAAAAZbWvbDgAAAA; stsservicecookie=estsppe'
    }
    response = requests.request("GET", login_url, headers=headers, data=payload).json()
    try:
        token_type = response["token_type"]
    except Exception as e:
        print(f"Bad response: {response}")
        raise e

    if token_type != "Bearer":
        raise ValueError("The token received is not a bearer.")

    return response["access_token"]


def create_workspace(endpointwl, bearer_token, username, capacity_id, user_id, workspace_name=None):
    user, tenant = username.split('@')
    url = f"https://{endpointwl}/metadata/folders"

    if workspace_name is None:
        workspace_name = f"Sempy_WS_{uuid4()}"

    print(f"Creating workspace: '{workspace_name}'")

    payload = json.dumps({
        "displayName": workspace_name,
        "capacityObjectId": capacity_id,
        "isServiceApp": False,
        "contacts": [
            {
                "displayName": f"{user} (Owner)",
                "userPrincipalName": username,
                "objectId": user_id,
                "emailAddress": username,
                "objectType": 1,
                "isSecurityGroup": False
            }
        ],
        "datasetStorageMode": 1,
        "domainObjectId": ""
        })

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {bearer_token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        workspace_id = response.json()["objectId"]
        print(f"Workspace '{workspace_name}', id: '{workspace_id}' has been created.")
    else:
        raise ConnectionError(f"Workspace '{workspace_name}'creation failed. Response {response.status_code}: {response.reason}, {response.text}")

    return workspace_id


def print_test_ntbk_output(response):
    cells = _get_ntbk_cells(response)

    pytest_failed = False
    for cell in cells:
        if cell['cell_type'] != 'code':
            continue
        outputs = cell["outputs"]
        for output in outputs:
            if output["output_type"] == "stream":
                print(output["text"])
            if "ExitCode.TESTS_FAILED" in str(output):
                pytest_failed = True

    if pytest_failed:
        raise RuntimeError("pytest returned ExitCode.TESTS_FAILED")


def print_ntbk_output(response):
    cells = _get_ntbk_cells(response)

    for cell in cells:
        if cell['cell_type'] != 'code':
            continue
        print(cell['source'])
        outputs = cell["outputs"]
        for output in outputs:
            if 'data' in output:
                data = output['data']
                if 'application/vnd.livy.statement-meta+json' not in data:
                    print(output['data']['text/plain'])
            if 'text' in output:
                print(output['text'])
        print()


def _get_ntbk_cells(response):
    result = response["result"]
    if result["runStatus"] != "Succeeded":
        print(result["error"])
        raise ValueError("Notebook run didn't succeed.")

    return result["snapshot"]["notebookContent"]["properties"]["cells"]
