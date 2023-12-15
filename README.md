# rubrik-rbs-upgrade
A Python script forces the upgrade of RBS clients.

## Dependencies

This projects requires the following libraries to work:
- `rubrik_cdm`
- `pandas`
- `tqdm`
- `getpass`

## How to use it.

1- Create a JSON file named `config.json`, inside the folder `configuration`, with your Rubrik Cluster information, like in the example below:
```
{
    "clusters": [
    {
        "cluster_address": "rubrik_cdm_ip_or_hostname",
        "api_token": "api_token_of_rubrik_cdm"
    },
    {
        "cluster_address": "192.158.10.3",
        "api_token": "really_long_api_string"
    },
    {
        "cluster_address": "rubrik3.mydomain.com",
        "api_token": "really_long_api_string_2"
    }
    ]
}
```
2- Download this repository and place in a computer or server that has access to your Rubrik CDMs

3- Install dependencies: `pip install -r requirements.txt`

4- Run main.py
