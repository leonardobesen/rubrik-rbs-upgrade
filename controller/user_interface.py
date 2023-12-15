import getpass


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
    password = getpass.getpass("Enter admin password: ")

    return {
        'user': user,
        'password': password
    }


def choose_action() -> int:
    print("Choose an action:")
    print("1. Get List of RBS version for clients")
    print("2. Upgrade RBS version")

    while True:
        try:
            choice = int(
                input("Enter the number corresponding to your choice: "))
            if choice in [1, 2]:
                return choice
            else:
                print("Invalid choice. Please enter 1 or 2.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def select_latest_version(hosts: list[dict]) -> str:
    versions = set()

    for host in hosts:
        versions.add(host["agentVersion"])

    sorted_versions = sorted(versions, reverse=True)

    print("Choose the LATEST RBS version")
    for i, version in enumerate(sorted_versions, start=1):
        print(f"{i}. {version}")

    while True:
        try:
            choice = int(
                input("Enter the number corresponding to your choice: "))
            if 1 <= choice <= len(sorted_versions):
                return sorted_versions[choice - 1]
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
