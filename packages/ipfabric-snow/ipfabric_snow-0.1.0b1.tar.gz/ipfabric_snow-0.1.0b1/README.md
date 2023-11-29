# ServiceNow Integration with IP Fabric
This project syncs devices from IP Fabric to Service Now. It ensures that the environment variables are properly set up before syncing the devices.

## Environment Setup
During the setup, you'll be prompted to enter the necessary environment variables including URLs and authentication details for both ServiceNow and IP Fabric.

You'll also be given an option to store sensitive data (passwords, tokens) in the .env file. If you choose not to store sensitive data in the .env file, you'll need to provide these details each time you run the sync command.

## Syncing Devices
To sync devices from IP Fabric to Service Now, run:

```bash
ipfabric-snow sync devices <staging_table_name>
```
If the environment is not properly set up, you'll be prompted to set it up. Follow the prompts to provide the necessary details.

```shell
ipfabric-snow --help
```
```shell
 Usage: ipfabric-snow [OPTIONS] COMMAND [ARGS]...                                                                                                                                                 
                                                                                                                                                                                                  
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --log-level                                 TEXT  Log level [default: INFO]                                                                                                                    │
│ --log-to-file           --no-log-to-file          Log to file [default: log-to-file]                                                                                                           │
│ --log-file-name                             TEXT  Log file name [default: ipf_serviceNow.log]                                                                                                  │
│ --log-json              --no-log-json             Log in JSON format [default: no-log-json]                                                                                                    │
│ --install-completion                              Install completion for the current shell.                                                                                                    │
│ --show-completion                                 Show completion for the current shell, to copy it or customize the installation.                                                             │
│ --help                                            Show this message and exit.                                                                                                                  │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ env                     Setup environment variables                                                                                                                                            │
│ sync                    Sync Inventory data with Service Now                                                                                                                                   │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
```shell
 ipfabric-snow sync devices --help
```
```shell                                                                                                                                                                  
 Usage: ipfabric-snow sync devices [OPTIONS] [STAGING_TABLE_NAME]                                                                                                                                 
                                                                                                                                                                                                  
 Sync devices from IP Fabric to Service Now                                                                                                                                                       
                                                                                                                                                                                                  
╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│   staging_table_name      [STAGING_TABLE_NAME]  The name of the Service Now staging table to use. [env var: SNOW_STAGING_TABLE_NAME] [default: None]                                           │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --show-diff          --no-show-diff                  Display the data difference [default: no-show-diff]                                                                                       │
│ --diff-source                               TEXT     Specify the main source for diff, either IPF or SNOW [default: IPF]                                                                       │
│ --write-diff         --no-write-diff                 Enable or disable writing the diff to a file [default: no-write-diff]                                                                     │
│ --diff-file                                 TEXT     Path to save the diff file, if desired [default: data/{date_time}_diff_{diff_source}.json]                                                │
│ --dry-run            --no-dry-run                    Perform a dry run without making any changes [default: no-dry-run]                                                                        │
│ --ipf-snapshot                              TEXT     IP Fabric snapshot ID to use for the sync [default: $last]                                                                                │
│ --cmdb-table-name                           TEXT     Name of the cmdb table to pull data from. Defaults to cmdb_ci_netgear [default: cmdb_ci_netgear]                                          │
│ --timeout                                   INTEGER  timeout for httpx requests [default: 10]                                                                                                  │
│ --output-verbose     --no-output-verbose             adds more detail to the output. Identifies which keys changed per device [default: no-output-verbose]                                     │
│ --help                                               Show this message and exit.                                                                                                               │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

example of sync devices command:
```shell
ipfabric-snow --log-level DEBUG sync devices --show-diff --diff-source SNOW  --ipf-snapshot "12dd8c61-129c-431a-b98b-4c9211571f89" --output-verbose u_ipf_inventory_devices --timeout 30
```