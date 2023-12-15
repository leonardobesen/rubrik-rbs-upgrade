import rubrik_cdm
import urllib3


def connect_to_cluster(cluster_adress: str, api_token: str) -> rubrik_cdm.Connect:
    # Disable HTTPS certificate warnings
    urllib3.disable_warnings()

    # Establish a connection to the Rubrik cluster
    rubrik = rubrik_cdm.Connect(node_ip=cluster_adress, api_token=api_token)

    return rubrik
