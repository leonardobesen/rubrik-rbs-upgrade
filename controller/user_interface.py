from getpass import getpass
import pandas as pd


def select_cluster(config):
    print("Available Clusters:")
    for i, cluster in enumerate(config['clusters'], start=1):
        print(f"{i}. {cluster['cluster_address']}")

    while True:
        try:
            choice = int(input("Select the cluster (enter the number): "))
            if 1 <= choice <= len(config['clusters']):
                return config['clusters'][choice - 1]
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_user_credentials():
    print("Please provide the Rubrik Cluster's admin credentials")
    user = input("Enter admin username: ")
    password = getpass("Enter admin password: ")

    return {
        'user': user,
        'password': password
    }


def choose_action() -> int:
    print("Choose an action:")
    print("1. Get List of RBS version for clients")
    print("2. Upgrade RBS version")
    print("3. Upgrade RBS version from csv file")

    while True:
        try:
            choice = int(
                input("Enter the number corresponding to your choice: "))
            if choice in [1, 2, 3]:
                return choice
            else:
                print("Invalid choice. Please enter 1, 2 or 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def select_latest_versions(hosts: list[dict] | pd.DataFrame) -> list[str]:
    versions = set()

    if isinstance(hosts, pd.DataFrame):
        for index, host in hosts.iterrows():
            versions.add(host["agentVersion"])
    elif isinstance(hosts, list):
        for host in hosts:
            versions.add(host["agentVersion"])

    sorted_versions = sorted(versions, reverse=True)

    print("Choose the LATEST RBS version")
    for i, version in enumerate(sorted_versions, start=1):
        print(f"{i}. {version}")

    selected_versions = []
    while True:
        try:
            choice = input(
                "Enter the number(s) corresponding to your choice(s), separated by commas (e.g., 1,2,3): ")
            choices = [int(c.strip()) for c in choice.split(',')]

            if all(1 <= c <= len(sorted_versions) for c in choices):
                selected_versions = [sorted_versions[c - 1] for c in choices]
                break
            else:
                print("Invalid choice. Please enter valid numbers separated by commas.")
        except ValueError:
            print("Invalid input. Please enter numbers separated by commas.")

    return selected_versions
