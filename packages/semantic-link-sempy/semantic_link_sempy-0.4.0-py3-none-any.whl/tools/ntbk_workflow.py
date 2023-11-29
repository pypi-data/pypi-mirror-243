import json
import os
import re
import requests
import sys
import time

from datetime import datetime, timedelta
from glob import glob
from tools.fabric_auth_util import FabricAuthUtil
from sempy.fabric._client._tools import upload_to_lakehouse
from tools.trident_utils import (
    env_cred,
    env_endpoint,
    env_capacity_id,
    env_my_workspace_id,
    env_named_workspace_id,
    env_onelake,
    env_onelake_new,
    env_ci_lakehouse_id,
    get_bearer_token,
    print_ntbk_output,
    print_test_ntbk_output,
)


def build_wheel():
    os.system("python setup.py bdist_wheel")

    whls = glob("dist/*.whl")
    if len(whls) > 1:
        raise RuntimeError("There is more than 1 whl in your dist dir. Delete the dir and try again.")

    whl_path = whls[0]

    return whl_path


def authenticate(username, password, env):
    if username.lower() != env_cred[env].lower():
        raise ValueError(f"'{username}' does not match '{env_cred[env]}' for environment '{env}'")

    return get_bearer_token(env, username, password)


def import_notebook(env, ntbk_path, whl_path, workspace_id, date, lakehouse_name="sempy_ci_lake"):

    print(f"Load json from {ntbk_path}...")
    ntbk_json = json.load(open(ntbk_path))

    print("Impute setup cells with a reference to the wheel...")
    ntbk_json = _impute_whl(ntbk_json, date, whl_path)

    print("Get rid of cells that are marked in metadata with fabric_skip_execution tag...")
    tags_to_clean = ['fabric_skip_execution']
    ntbk_json = _clean_tagged_cells(ntbk_json, tags_to_clean)

    print("Impute lakehouse metadata...")
    ntbk_json = _impute_lakehouse_metadata(ntbk_json, lakehouse_name, env_ci_lakehouse_id[env], env_named_workspace_id[env])

    url = f"https://{env_endpoint[env]}/metadata/workspaces/{workspace_id}/artifacts"

    ntbk = ntbk_path.split('/')[-1].split('.')[0]
    ntbk_name = f"{ntbk}_{date}"

    payload = json.dumps({
        "artifactType": "SynapseNotebook",
        "description": "New notebook",
        "displayName": ntbk_name,
        "workloadPayload": json.dumps(ntbk_json),
        "payloadContentType": "InlinePlainText"
        })

    headers = {
        'Authorization': f'Bearer {pbi_token}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 202:
        print(f"Notebook '{ntbk_name}' created.")
    else:
        raise RuntimeError(f"Notebook '{ntbk_name}' creation failed: {response.status_code}: {response.text}")

    attempts = 0
    sleep_factor = 1.5
    while attempts < 10:
        response = requests.request("GET", url, headers=headers, data=payload).json()
        ntbk_prov = response[-1]
        prov_state = ntbk_prov["provisionState"]
        if prov_state == "Active":
            notebook_id = ntbk_prov["objectId"]
            break
        print(f"Notebook Provision State: {prov_state}")
        time.sleep(sleep_factor ** attempts)
        attempts += 1

    if attempts == 10:
        raise TimeoutError(f"Notebook '{ntbk_name}' upload to workspace timed out.")

    print(f"Finish import of '{ntbk_name}', path: {ntbk_path}")

    return ntbk_name, notebook_id


def _create_lakehouse(workspace_id, endpointwl, bearer_token, runner_type, commit_id):
    lh_name = f"Lakehouse_{runner_type}_{commit_id}"
    print(f"Start creation of lakehouse {lh_name}")

    url = f"https://{endpointwl}/metadata/workspaces/{workspace_id}/artifacts"

    payload = json.dumps({
        "artifactType": "Lakehouse",
        "displayName": lh_name
    })

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {bearer_token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        lakehouse_id = response.json()["objectId"]
        print(f"Created Lakehouse: '{lh_name}', id: {lakehouse_id}")
    elif response.json()["error"]["code"] == "PowerBIMetadataArtifactDisplayNameInUseException":
        print(f"Lakehouse '{lh_name}' already exists, rerun of ntbk_workflow tool. Continuing execution...")

        payload = json.dumps({"supportedTypes": ["Lakehouse"],
                              "tridentSupportedTypes": ["Lakehouse"],
                              "pageNumber": 1,
                              "pageSize": 10000,
                              "filters": [],
                              "orderDirection": ""})

        url = f"https://{endpointwl}/metadata/datahub/V2/artifacts"
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            for lakehouse in response.json():
                if lakehouse["displayName"] == lh_name:
                    lakehouse_id = lakehouse["artifactObjectId"]

                    return lh_name, lakehouse_id
        else:
            raise ConnectionError(f"Lakehouse '{lh_name}' lookup failed. Response {response.status_code}: {response.json()}")

    else:
        raise ConnectionError(f"Lakehouse '{lh_name}' creation failed. Response {response.status_code}: {response.json()}")

    return lh_name, lakehouse_id


def delete_artifact(env, name, id, bearer_token):
    print(f"Start delete of artifact {name}: {id}")

    url = f"https://{env_endpoint[env]}/metadata/artifacts/{id}"

    payload = {}
    headers = {
        'Authorization': f'Bearer {bearer_token}'
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)

    if response.status_code != 200:
        raise RuntimeError(f"Artifact {name} failed to delete. Response: {response.json()}")

    print(f"Artifact {name} is now deleted.")


def _delete_workspace(workspace_id, endpointwl, bearer_token):
    url = f"https://{endpointwl}/metadata/folders/{workspace_id}"

    payload = json.dumps({})

    headers = {
        'Authorization': f'Bearer {bearer_token}'
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)

    if response.status_code != 204:
        raise ConnectionError(f"Workspace {workspace_id} failed to delete. Response: {response.json()}")

    print(f"Workspace {workspace_id} is now deleted.")


def run_notebook(env, notebook_id, workspace_id, bearer_token):
    # Submit run notebook request
    url = f"https://{env_endpoint[env]}/metadata/artifacts/{notebook_id}/jobs/RunNotebook"
    payload = json.dumps({})
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload, timeout=5)

    if response.status_code == 202:
        print("Run Notebook request accepted.")
    else:
        raise ConnectionError(f"Run notebook request was not accepted. Response: {response.json()}")

    run_id = response.json()["artifactJobInstanceId"]

    start_time = time.time()
    print(f"Start Time: {start_time}")
    exec_secs_max = 3600
    timeout = start_time + exec_secs_max

    # Query Notebook Status
    url = f"https://{env_endpoint[env]}/metadata/artifacts/{notebook_id}/jobs/{run_id}"
    payload = json.dumps({})
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json'
    }
    while True:
        if time.time() > timeout:
            raise TimeoutError(f"Notebook didn't complete within {exec_secs_max} seconds. Terminating run.")

        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code != 200 and response.status_code != 404:
            raise ConnectionError(f"Unable to query status of notebook. Response: {response.json()}")

        try:
            response_json = response.json()
            if response_json is None:
                print(f"Status: {response.status_code}")
            else:
                if response_json["isSuccessful"] and response_json["statusString"] == 'Completed':
                    print(f"Notebook completed in {time.time() - start_time} seconds.")
                    break
                print(f"Status: {response_json['statusString']}")
            time.sleep(10)
        except Exception:
            raise ConnectionError(f"Bad response: '{response.text}'")

    # Get MWC Token
    url = f"https://{env_endpoint[env]}/metadata/v201606/generatemwctoken"
    payload = json.dumps({
        "capacityObjectId": f"{env_capacity_id[env]}",
        "workspaceObjectId": f"{workspace_id}",
        "workloadType": "Notebook",
        "artifactObjectIds": [
            f"{notebook_id}"
        ]
    })
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        print("MWC Token Found")
    else:
        raise ConnectionError(f"Error in getting MWC Token. Response: {response.json()}")

    mwc_token = response.json()["Token"]
    target_uri_host = response.json()["TargetUriHost"]

    # get notebook snapshot/results
    url = f"https://{target_uri_host}/webapi/capacities/{env_capacity_id[env]}/workloads/Notebook/Data/Direct/api/workspaces/{workspace_id}/artifacts/{notebook_id}/snapshot/{run_id}"
    payload = json.dumps({})
    headers = {
        'Authorization': f'mwctoken {mwc_token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code != 200:
        raise ConnectionError(f"Unable to get notebook snapshot. Response: {response.json()}")

    return response.json()


def _impute_whl(ntbk_json, date, whl_path):
    pip_cell = {
            "cell_type": "code",
            "metadata": {},
            "outputs": [],
            "execution_count": None,
            "source": [
                f"date = '{date}'\n",
                f"whl_path = '{whl_path}'\n"
                "\n"
                "import pip\n",
                "pip.main(['install', f'/lakehouse/default/Files/{date}/{whl_path}'])"
            ]
        }

    # insert at the very beginning so it's not dependent on any other cells
    ntbk_json["cells"].insert(0, pip_cell)

    return ntbk_json


def _clean_tagged_cells(ntbk_json, tags_to_clean):
    for cell in ntbk_json['cells']:
        for tag in tags_to_clean:
            if tag in cell['metadata'].get('tags', []):
                ntbk_json['cells'].remove(cell)

    return ntbk_json


def _impute_lakehouse_metadata(ntbk_json, lakehouse_name, lakehouse_id, workspace_id):
    ntbk_json["metadata"]["trident"] = {
            "lakehouse": {
                "default_lakehouse": lakehouse_id,
                "known_lakehouses": [
                    {
                        "id": lakehouse_id
                    }
                ],
                "default_lakehouse_name": lakehouse_name,
                "default_lakehouse_workspace_id": workspace_id
            }
        }

    return ntbk_json


def cleanup(env, workspace_id, now, pbi_token, storage_token):
    print("Start fabric cleanup...")

    print(f"Start workspace {workspace_id} artifact cleanup..")
    url = f"https://{env_endpoint[env]}/metadata/workspaces/{workspace_id}/artifacts"
    payload = {}
    headers = {
        'Authorization': f'Bearer {pbi_token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code != 200:
        raise ConnectionError(f"Artifact listing failed. Response {response.status_code}: {response.reason}, {response.text}")

    for artifact in response.json():
        date_match = re.search(r"\d{4}_\d{2}_\d{2}T\d{2}_\d{2}_\d{2}$", artifact["displayName"])
        if date_match and datetime.strptime(date_match.group().upper(), '%Y_%m_%dT%H_%M_%S') < now - timedelta(days=1):
            delete_artifact(env, artifact["displayName"], artifact["objectId"], pbi_token)
    print(f"Finish {workspace_id} artifact cleanup...")

    cleanup_lakehouse(env, now, storage_token)

    print("Finish fabric cleanup...")


def cleanup_lakehouse(env, now, storage_token):
    print(f"Start {env} lakehouse cleanup ...")
    groups = ['Tables', 'Files']
    payload = {}
    headers = {
        'Authorization': f'Bearer {storage_token}'
    }

    for grp in groups:
        workspace_url = f"https://{env_onelake_new[env]}/{env_named_workspace_id[env]}"
        list_url = f"{workspace_url}?recursive=false&resource=filesystem&directory={env_ci_lakehouse_id[env]}%2F{grp}&getShortcutMetadata=true"
        response = requests.request("GET", list_url, headers=headers, data=payload)
        if response.status_code != 200:
            raise RuntimeError(f"List {grp} in lakehouse {env_ci_lakehouse_id[env]} failed. Response {response.status_code}: {response.reason}, {response.text}")
        contents = response.json()["paths"]
        for item in contents:
            date_match = re.search(r"\d{4}_\d{2}_\d{2}T\d{2}_\d{2}_\d{2}$", item['name'], re.IGNORECASE)
            if date_match and datetime.strptime(date_match.group().upper(), '%Y_%m_%dT%H_%M_%S') < now - timedelta(days=1):
                recursive = True if item['isDirectory'] == "true" else False
                delete_lakehouse_dir(env, item['name'], storage_token, recursive)
    print(f"Finish {env} lakehouse cleanup ...")


def delete_lakehouse_dir(env, dir, storage_token, recursive=False):
    print(f"Deleting lakehouse dir {dir}...")
    workspace_url = f"https://{env_onelake_new[env]}/{env_named_workspace_id[env]}"
    delete_url = f"{workspace_url}/{dir}?recursive={str(recursive).lower()}"
    payload = {}
    headers = {
        'Authorization': f'Bearer {storage_token}'
    }
    response = requests.request("DELETE", delete_url, headers=headers, data=payload)
    if response.status_code != 200:
        raise RuntimeError(f"Delete {dir} failed. Response {response.status_code}: {response.reason}, {response.text}")

    print(f"Lakehouse dir {dir} deleted...")


if __name__ == "__main__":
    if len(sys.argv) != 6 and len(sys.argv) != 4:
        print("Usage: python tools/ntbk_workflow.py <env> <runner_type> <workspace> [<username> <password>]")
        sys.exit(2)

    env = sys.argv[1]

    runner_type = sys.argv[2]
    if runner_type != "notebooks" and runner_type != "unit_test":
        raise ValueError("<runner_type> must be 'notebooks' or 'unit_test'.")

    workspace = sys.argv[3]

    if len(sys.argv) == 6:
        username = sys.argv[4]
        password = sys.argv[5]
    else:
        auth_util = FabricAuthUtil(env)
        username = auth_util.get_env_username()
        password = auth_util.get_env_password()

    if workspace == "ci_workspace":
        workspace_id = env_named_workspace_id[env]
    elif workspace == "my_workspace":
        workspace_id = env_my_workspace_id[env]
    else:
        workspace_id = workspace

    pbi_token = authenticate(username, password, env)
    storage_token = get_bearer_token(env, username, password, audience="storage")
    now = datetime.utcnow()
    cleanup(env, workspace_id, now, pbi_token, storage_token)

    whl_path = build_wheel()
    date = now.strftime('%Y_%m_%dT%H_%M_%S')

    print(f"Uploading whl to lakehouse: {whl_path}")

    upload_to_lakehouse(whl_path, env_named_workspace_id[env], env_ci_lakehouse_id[env], env_onelake[env], storage_token, date)

    if runner_type == 'notebooks':
        ntbks = [
            "tests/notebooks/powerbi_dependencies.ipynb",
            "tests/notebooks/powerbi_relationships.ipynb",
            "tests/notebooks/powerbi_measures.ipynb",
            "tests/notebooks/powerbi_dax_magics.ipynb",
        ]
        storage_token = None
    elif runner_type == 'unit_test':
        ntbks = ["tests/UnitTestRunner.ipynb"]
        upload_to_lakehouse("tests", env_named_workspace_id[env], env_ci_lakehouse_id[env], env_onelake[env], storage_token, date)
        upload_to_lakehouse("tools", env_named_workspace_id[env], env_ci_lakehouse_id[env], env_onelake[env], storage_token, date)
        upload_to_lakehouse("pytest.ini", env_named_workspace_id[env], env_ci_lakehouse_id[env], env_onelake[env], storage_token, date)

    for nb in ntbks:
        print(f"Starting notebook run for {nb}")
        ntbk_name, ntbk_id = import_notebook(env, nb, whl_path, workspace_id, date)
        response_json = run_notebook(env, ntbk_id, workspace_id, pbi_token)
        if runner_type == "unit_test":
            print_test_ntbk_output(response_json)
            test_dir = f"{env_ci_lakehouse_id[env]}/Files/{date}"
            delete_lakehouse_dir(env, test_dir, storage_token, recursive=True)
        else:
            print_ntbk_output(response_json)
        # figure out the json that can be passed as middle param
        delete_artifact(env, ntbk_name, ntbk_id, pbi_token)
        print(f"Finished notebook run for {nb}")
