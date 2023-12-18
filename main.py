import os
import connection.connect as connect
import configuration.config as config
import controller.user_interface as user_interface
import controller.operations as operation
import pandas

# Global variables
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_PATH = os.path.join(ROOT_DIR, 'reports')
CONFIG_FILE = os.path.join(ROOT_DIR, 'configuration', 'config.json')


if __name__ == '__main__':

    clusters_info = config.read_config(CONFIG_FILE)
    cluster = user_interface.select_cluster(clusters_info)
    credentials = user_interface.get_user_credentials()

    # Establish connection with Rubrik CDM and Cluster name
    rubrik_conn = connect.connect_to_cluster(
        cluster['cluster_address'], cluster['api_token'])

    action_choice = user_interface.choose_action()

    if action_choice == 1:
        print("Get list of RBS version for clients")
        operation.list_all_host(rubrik_conn, credentials, REPORT_PATH)
    elif action_choice == 2:
        print("Perform Upgrade to RBS version")
        hosts = operation.list_all_host(rubrik_conn, credentials, REPORT_PATH)
        operation.upgrade_to_latest_version(rubrik_conn, credentials, hosts)
    elif action_choice == 3:
        print("Perform Upgrade to RBS version using CSV file")
        file_name = input("Type file name from reports folders: ")
        hosts = operation.list_all_host_from_csv(REPORT_PATH, file_name)
        operation.upgrade_to_latest_version(rubrik_conn, credentials, hosts)

    print("Process ended successfully")
    exit(0)
