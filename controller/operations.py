import rubrik_cdm
from tqdm import tqdm
import view.write_to_csv as write_to_csv
import controller.user_interface as user_interface
import pandas as pd
import os


def _get_all_hostnames(rubrik_conn: rubrik_cdm.Connect) -> list[str]:
    hostnames = []

    try:
        params = {}
        params['operating_system_type'] = 'ANY'
        params['sort_by'] = 'hostname'
        params['sort_order'] = 'asc'
        hosts = rubrik_conn.get('v1', f'/host', params=params)
    except:
        print("ERROR: Unable to list hosts")
        exit(1)

    if not hosts or not hosts["data"]:
        print("ERROR: Unable to list hosts")
        exit(1)

    for host in hosts["data"]:
        if not host["hostname"]:
            continue
        hostnames.append(host["hostname"])

    return hostnames


def list_all_host(rubrik_conn: rubrik_cdm.Connect, credentials: dict[str, str], REPORT_PATH=None) -> list[dict]:
    hostnames = _get_all_hostnames(rubrik_conn)
    hosts_infomation = []

    for host in tqdm(hostnames, desc="Querying RBS on hosts"):
        try:
            host_info = rubrik_conn.get(
                'v1', f'/host/rbs?name={host}&username={credentials["user"]}&password={credentials["password"]}&operation_timeout=600')
            hosts_infomation.append(host_info)
        except:
            print(f"ERROR: Unable to list host {host}")
            continue

    if REPORT_PATH:
        write_to_csv.create_file(
            rubrik_conn, REPORT_PATH, hosts_infomation)

    return hosts_infomation


def list_all_host_from_csv(REPORT_PATH: str, file_name: str) -> list[dict]:
    file_path = os.path.join(REPORT_PATH, file_name)
    hosts_infomation = pd.read_csv(file_path, encoding='utf-8', dtype=str)

    return hosts_infomation


def upgrade_to_latest_version(rubrik_conn: rubrik_cdm.Connect, credentials: dict[str, str], hosts: list[dict] or pd.DataFrame):
    hostnames = []

    latest_versions = user_interface.select_latest_versions(hosts)

    if isinstance(hosts, pd.DataFrame):
        for index, host in hosts.iterrows():
            if host["agentVersion"] in latest_versions:
                continue
            hostnames.append(host["name"])
    elif isinstance(hosts, list):
        for host in hosts:
            if host["agentVersion"] in latest_versions:
                continue
            hostnames.append(host["name"])
    else:
        raise ValueError(
            "Unsupported type for 'hosts'. It should be a DataFrame or a list of dictionaries.")

    _upgrade_rbs(rubrik_conn, credentials, hostnames)


def _upgrade_rbs(rubrik_conn: rubrik_cdm.Connect, credentials: dict[str, str], hostnames: list[str]):
    for host in tqdm(hostnames, desc="Upgrading RBS on hosts"):
        request = {}
        request["name"] = host
        request["username"] = credentials["user"]
        request["password"] = credentials["password"]
        request["operationTimeout"] = 600
        request["operationMode"] = "Asynchronous"
        try:
            rubrik_conn.post('v1', f'/host/rbs/upgrade', config=request)
        except:
            print(f"Unable to start RBS upgrade on {host}")
