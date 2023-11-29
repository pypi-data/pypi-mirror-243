<!-- This file is auto-generated -->

# Prodigy Teams CLI

Before using Prodigy Teams CLI you need to have a **Prodigy Teams** account. You also need a deployed cluster and Python 3.6+. To see all available commands or subcommands, you can use the `--help` flag, e.g. `ptc --help`.

## `ptc`

Prodigy Teams Command Line Interface.

### `ptc actions`

Interact with actions on the cluster

#### `ptc actions create`

Create a new action. The available action recipes are fetched from your cluster and are added as dynamic subcommands. You can see more details and available arguments by calling the subcommand with --help, e.g. create [name] --help

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `--exists-ok` | `bool` | Don't raise an error if it exists | `False` |
| `--no-start` | `bool` | Don't start {noun} after creation | `False` |
| `--help`, `-h` | `bool` | Show help message | `False` |
| `_extra` | `List[str]` |  | `[]` |

#### `ptc actions list`

List the actions on the cluster. By default, this includes their ID, name and current state, e.g. created or completed

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `--select` | `List[str]` | Comma-separated fields to select and show in output. Available: ['id', 'created', 'updated', 'is_running', 'is_startable', 'is_stoppable', 'broker_id', 'name', 'project_id', 'job_type', 'state', 'plan', 'cli_command', 'stats'] | `['id', 'name', 'state']` |
| `--json` | `bool` | Output the result as JSON | `False` |

#### `ptc actions info`

Print information about an action on the cluster

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name_or_id` | `Union[str, UUID]` | Name or ID of the action |  |
| `project_id` | `UUID` | ID of action's project (or the last project if not set) | `None` |
| `cluster_id` | `UUID` | ID of the cluster to search for action name (or the last cluster if not set) | `None` |
| `--select` | `List[str]` | Comma-separated fields to select and show in output. Available: ['id', 'created', 'updated', 'is_running', 'is_startable', 'is_stoppable', 'broker_id', 'name', 'project_id', 'job_type', 'state', 'plan', 'cli_command', 'stats', 'recipe_name', 'recipe_title', 'evaluation', 'project_name', 'error', 'executions', 'last_execution_id', 'nomad_index', 'url_logs', 'url', 'related_tasks', 'created_by_user'] | `None` |
| `--json` | `bool` | Output the result as JSON | `False` |

#### `ptc actions logs`

Get logs for an action on the cluster

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name_or_id` | `str` | Name or ID of the action (or the last action if not set) | `None` |
| `project_id` | `UUID` | ID of action's project (or the last project if not set) | `None` |
| `cluster_id` | `UUID` | ID of the cluster to search for action name (or the last cluster if not set) | `None` |
| `--json` | `bool` | Output the result as JSON | `False` |

#### `ptc actions start`

Start an action on the cluster

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name_or_id` | `str` | Name or ID of the action (or the last action if not set) | `None` |
| `project_id` | `UUID` | ID of action's project (or the last project if not set) | `None` |
| `cluster_id` | `UUID` | ID of the cluster to search for action name (or the last cluster if not set) | `None` |
| `--worker-class` | `str` | Worker class to launch the action on. Generally one of: ['medium', 'large', 'gpu'] | `None` |

#### `ptc actions stop`

Stop an action on the cluster

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name_or_id` | `str` | Name or ID of the action (or the last action if not set) | `None` |
| `project_id` | `UUID` | ID of action's project (or the last project if not set) | `None` |
| `cluster_id` | `UUID` | ID of the cluster to search for action name (or the last cluster if not set) | `None` |

#### `ptc actions delete`

Delete an Action by name or ID

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name_or_id` | `Union[str, UUID]` | Name or ID of the action |  |
| `project_id` | `UUID` | ID of action's project (or the last project if not set) | `None` |
| `cluster_id` | `UUID` | ID of the cluster to search for action name (or the last cluster if not set) | `None` |

### `ptc assets`

View and manage assets on the cluster

#### `ptc assets list`

List all assets on the cluster registered with Prodigy Teams

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `--select` | `List[str]` | Comma-separated fields to select and show in output. Available: ['id', 'created', 'updated', 'broker_id', 'name', 'version', 'kind', 'path', 'meta', 'num_used_by'] | `['id', 'name', 'kind']` |
| `--json` | `bool` | Output the result as JSON | `False` |

#### `ptc assets info`

Get detailed info for an asset uploaded to the cluster and registered with Prodigy Teams

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name_or_id` | `Union[str, UUID]` | Name or ID of the asset |  |
| `project_id` | `UUID` | ID of action's project (or the last project if not set) | `None` |
| `cluster_id` | `UUID` | ID of the cluster to search for action name (or the last cluster if not set) | `None` |
| `--select` | `List[str]` | Comma-separated fields to select and show in output. Available: ['id', 'created', 'updated', 'broker_id', 'name', 'version', 'kind', 'path', 'meta', 'num_used_by', 'tasks', 'actions'] | `None` |
| `--json` | `bool` | Output the result as JSON | `False` |

#### `ptc assets create`

Create an asset on the cluster and register it with Prodigy Teams. Assets point to files or directories you control. The Prodigy Teams server only has a reference to them. This command doesn't transfer any data. See `ptc files` for utilities to transfer files to and from your cluster

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name` | `str` | Name of the asset |  |
| `--kind` | `str` | Kind of the asset. Generally one of: ['Input', 'Model', 'Patterns] |  |
| `path` | `str` | Path of the asset |  |
| `--version` | `str` | Version of the asset | `'0.0.0'` |
| `--meta` | `str` | Asset meta, formatted as a JSON string | `'{}'` |
| `--exists-ok` | `bool` | Don't raise an error if it exists | `False` |

#### `ptc assets delete`

Delete an asset registered with Prodigy Teams

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name_or_id` | `Union[str, UUID]` | Name or ID of the asset |  |
| `project_id` | `UUID` | ID of asset's project (or the last project if not set) | `None` |
| `cluster_id` | `UUID` | ID of the cluster to search for asset name (or the last cluster if not set) | `None` |

### `ptc clusters`

Interact with clusters

#### `ptc clusters list`

List resources on the cluster

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `--select` | `List[str]` | Comma-separated fields to select and show in output. Available: ['id', 'created', 'updated', 'org_id', 'name', 'address', 'state', 'cloud_provider', 'cloud_account', 'cloud_region', 'client_id', 'client_secret'] | `['id', 'name', 'status', 'address']` |
| `--json` | `bool` | Output the result as JSON | `False` |

#### `ptc clusters info`

Get detailed info for a cluster

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name_or_id` | `Union[str, UUID]` | Name or ID of the cluster |  |
| `--select` | `List[str]` | Comma-separated fields to select and show in output. Available: ['id', 'created', 'updated', 'org_id', 'name', 'address', 'state', 'cloud_provider', 'cloud_account', 'cloud_region', 'client_id', 'client_secret', 'worker_classes'] | `None` |
| `--json` | `bool` | Output the result as JSON | `False` |

#### `ptc clusters update`

Update the cluster info

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name_or_id` | `Union[str, UUID]` | Name or ID of the cluster |  |
| `--new-name` | `str` | New name of the cluster | `None` |
| `--address` | `str` | New address of the cluster | `None` |
| `--json` | `bool` | Output the result as JSON | `False` |

#### `ptc clusters delete`

Delete a cluster from PAM. This only removes PAM's record of it. The cluster itself will continue to exist - you need to shut it down separately.

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name_or_id` | `Union[str, UUID]` | Name or ID of the cluster |  |

#### `ptc clusters check`

Check the cluster deployment went well

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `--s3-bucket` | `str` | Run checks involving the S3 storage | `None` |
| `--nfs-path` | `str` | Run checks involving the NFS storage | `None` |
| `--recipe` | `str` | Run checks that need to operate over a recipe. This argument only makes sense when used with --recipe-args | `None` |
| `--recipe-args` | `str` | Run checks that need to operate over a recipe. This argument only makes sense when used with --recipe | `None` |

### `ptc config`

Configure the CLI

#### `ptc config reset`

Reset all caching and configuration.

#### `ptc config project`

Set the default project.

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name_or_id` | `Union[str, UUID]` | Name or ID of the project |  |

#### `ptc config task`

Set the default task.

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name_or_id` | `Union[str, UUID]` | Name or ID of the task |  |
| `project_id` | `UUID` | ID of task's project (or the last project if not set) | `None` |
| `cluster_id` | `UUID` | ID of the cluster to search for task name (or the last cluster if not set) | `None` |

#### `ptc config action`

Set the default action.

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name_or_id` | `Union[str, UUID]` | Name or ID of the action |  |
| `project_id` | `UUID` | ID of action's project (or the last project if not set) | `None` |
| `cluster_id` | `UUID` | ID of the cluster to search for action name (or the last cluster if not set) | `None` |

#### `ptc config set-cluster-host`

Set the broker cluster host.

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `host` | `str` | Host or URL of the cluster |  |

#### `ptc config set-pam-host`

Set the PAM host.

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `host` | `str` | Host or URL of the Prodigy Annotation Manager (PAM) app |  |

### `ptc datasets`

View and manage Prodigy datasets on the cluster

#### `ptc datasets list`

List all Datasets

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `--select` | `List[str]` | Comma-separated fields to select and show in output. Available: ['id', 'created', 'updated', 'name', 'broker_id', 'kind', 'num_used_by'] | `['id', 'name', 'kind']` |
| `--json` | `bool` | Output the result as JSON | `False` |

#### `ptc datasets info`

Get detailed info for a Dataset

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name_or_id` | `Union[str, UUID]` | Name or ID of the dataset |  |
| `cluster_id` | `UUID` | ID of the cluster to search for dataset name (or the last cluster if not set) | `None` |
| `--select` | `List[str]` | Comma-separated fields to select and show in output. Available: ['id', 'created', 'updated', 'name', 'broker_id', 'kind', 'num_used_by', 'tasks', 'actions'] | `None` |
| `--json` | `bool` | Output the result as JSON | `False` |

#### `ptc datasets create`

Create a new dataset

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name` | `str` | Name of the dataset |  |
| `--kind` | `str` | Kind of the dataset, used to filter in recipes to only allow specific types |  |
| `--exists-ok` | `bool` | Don't raise an error if it exists | `False` |

#### `ptc datasets delete`

Delete a dataset

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name_or_id` | `Union[str, UUID]` | Name or ID of the dataset |  |
| `cluster_id` | `UUID` | ID of the cluster to search for dataset name (or the last cluster if not set) | `None` |

#### `ptc datasets export`

Export all the examples from a dataset and save it in the designated file as JSONL (newline-delimited JSON).

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name_or_id` | `Union[str, UUID]` | Name or ID of the dataset |  |
| `--output`, `-o` | `str` | JSON output path for data | `'-'` |

### `ptc files`

Manage files on the cluster. Your files are only ever sent to servers or buckets you control. They are never sent to our servers.

#### `ptc files cp`

Copy files to and from the cluster

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `src` | `str` | Remote or local path of the source |  |
| `dest` | `str` | Remote or local path of the destination |  |
| `--recurse`, `-r` | `bool` | Copy whole directory recursively | `False` |
| `--make-dirs` | `bool` | Create parent directories if they don't exist | `False` |
| `--overwrite` | `bool` | Overwrite if exists | `False` |
| `--cluster-host` | `str` | Name of the cluster (or the last cluster if not set) | `None` |

#### `ptc files ls`

List the files under `remote`

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `remote` | `str` | Remote location path |  |
| `--recurse`, `-r` | `bool` | List files recursively | `False` |
| `--json` | `bool` | Output the result as JSON | `False` |
| `--cluster-host` | `str` | Name of the cluster (or the last cluster if not set) | `None` |
| `--expand-path-aliases` | `bool` | Expand path aliases when displaying remote paths | `False` |

#### `ptc files rm`

Remove files from the cluster

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `remote_path` | `str` | Remote location path |  |
| `--cluster-host` | `str` | Name of the cluster (or the last cluster if not set) | `None` |
| `--missing-ok` | `bool` | If missing, don't raise an error | `False` |
| `--recurse`, `-r` | `bool` | Delete the whole directory recursively | `False` |

#### `ptc files rsync`

Rsync files to and from the cluster

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `src` | `str` | Remote or local path of the source |  |
| `dest` | `str` | Remote or local path of the destination |  |
| `--cluster-host` | `str` | Name of the cluster (or the last cluster if not set) | `None` |

#### `ptc files stats`

Get the stats for a file located in `remote_path`

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `remote_path` | `str` | Remote location path |  |
| `--cluster-host` | `str` | Name of the cluster (or the last cluster if not set) | `None` |
| `--json` | `bool` | Output the result as JSON | `False` |

### `ptc packages`

View and manage Python packages on the cluster

#### `ptc packages list`

List all packages

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `--select` | `List[str]` | Comma-separated fields to select and show in output. Available: ['id', 'created', 'updated', 'name', 'version', 'environment', 'num_used_by', 'recipe_count'] | `['id', 'name', 'version', 'recipe_count', 'num_used_by']` |
| `--json` | `bool` | Output the result as JSON | `False` |

#### `ptc packages info`

Get detailed info for a package

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name_or_id` | `Union[str, UUID]` | Name or ID of the package |  |
| `cluster_id` | `UUID` | ID of the cluster to search for package name (or the last cluster if not set) | `None` |
| `--select` | `List[str]` | Comma-separated fields to select and show in output. Available: ['id', 'created', 'updated', 'name', 'version', 'environment', 'num_used_by', 'recipe_count', 'org_id', 'filename', 'meta', 'tasks', 'actions', 'author'] | `None` |
| `--json` | `bool` | Output the result as JSON | `False` |

#### `ptc packages create`

Create a new package

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name` | `str` | Name of the package |  |
| `--kind` | `str` | Kind of the package, used to filter in recipes to only allow specific types |  |
| `--exists-ok` | `bool` | Don't raise an error if it exists | `False` |

#### `ptc packages delete`

Delete a package

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name_or_id` | `Union[str, UUID]` | Name or ID of the package |  |
| `cluster_id` | `UUID` | ID of the cluster to search for package name (or the last cluster if not set) | `None` |
| `--force` | `bool` | Delete related actions or tasks as well | `False` |

### `ptc paths`

View and manage path aliases on the cluster

#### `ptc paths list`

List all cluster path aliases

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `--select` | `List[str]` | Comma-separated fields to select and show in output. Available: ['id', 'created', 'updated', 'broker_id', 'name', 'path'] | `['created', 'id', 'name', 'path']` |
| `--json` | `bool` | Output the result as JSON | `False` |

#### `ptc paths info`

Get detailed info for a path alias

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name_or_id` | `Union[str, UUID]` | Name or ID of the path |  |
| `cluster_id` | `UUID` | ID of the cluster to search for path name (or the last cluster if not set) | `None` |
| `--select` | `List[str]` | Comma-separated fields to select and show in output. Available: ['id', 'created', 'updated', 'broker_id', 'name', 'path'] | `None` |
| `--json` | `bool` | Output the result as JSON | `False` |

#### `ptc paths create`

Create a new path alias

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name` | `str` | Name of the path |  |
| `path` | `str` | Path of the cluster directory |  |
| `--exists-ok` | `bool` | Don't raise an error if it exists | `False` |

#### `ptc paths delete`

Delete a path alias

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name_or_id` | `Union[str, UUID]` | Name or ID of the path |  |
| `cluster_id` | `UUID` | ID of the cluster to search for path name (or the last cluster if not set) | `None` |

### `ptc projects`

View and manage Prodigy Teams projects

#### `ptc projects list`

List all projects

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `--select` | `List[str]` | Comma-separated fields to select and show in output. Available: ['id', 'created', 'updated', 'org_id', 'name', 'description'] | `['id', 'name']` |
| `--name` | `str` | Filter by name | `None` |
| `--json` | `bool` | Output the result as JSON | `False` |

#### `ptc projects info`

Get detailed info for a project

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name_or_id` | `Union[str, UUID]` | Name or ID of the project |  |
| `--select` | `List[str]` | Comma-separated fields to select and show in output. Available: ['id', 'created', 'updated', 'org_id', 'name', 'description'] | `None` |
| `--json` | `bool` | Output the result as JSON | `False` |

#### `ptc projects create`

Create a new project

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name` | `str` | Name of the project |  |
| `description` | `str` | Description of the project |  |
| `--exists-ok` | `bool` | Don't raise an error if it exists | `False` |

#### `ptc projects delete`

Delete a project

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name_or_id` | `Union[str, UUID]` | Name or ID of the project |  |

### `ptc recipes`

View and manage annotation recipe packages on the cluster

#### `ptc recipes list`

List all recipes

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `--select` | `List[str]` | Comma-separated fields to select and show in output. Available: ['id', 'created', 'updated', 'org_id', 'package_id', 'name', 'title', 'description', 'is_action', 'entry_point', 'num_used_by'] | `['id', 'name']` |
| `--json` | `bool` | Output the result as JSON | `False` |

#### `ptc recipes info`

Show info about a recipe

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name_or_id` | `Union[str, UUID]` | Name or ID of the recipe |  |
| `cluster_id` | `UUID` | ID of the cluster to search for recipe name (or the last cluster if not set) | `None` |
| `--select` | `List[str]` | Comma-separated fields to select and show in output. Available: ['id', 'created', 'updated', 'org_id', 'package_id', 'name', 'title', 'description', 'is_action', 'entry_point', 'num_used_by', 'form_schema', 'cli_schema', 'meta', 'tasks', 'actions', 'package'] | `None` |
| `--json` | `bool` | Output the result as JSON | `False` |

#### `ptc recipes init`

Generate a new recipes Python package

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `output_dir` | `Path` | Output directory for the recipe package |  |
| `--name` | `str` | Name of the package (e.g. custom_recipes) | `None` |
| `--version` | `str` | Version of the package | `'0.1.0'` |
| `--description` | `str` | Description of the package | `''` |
| `--author` | `str` | Name of the package author | `''` |
| `--email` | `str` | Email of the package author | `''` |
| `--url` | `str` | URL of the package | `''` |
| `--license` | `str` | License of the package | `''` |

### `ptc secrets`

View and manage named pointers to secrets on the cluster

#### `ptc secrets list`

List all named pointers to secrets on the cluster

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `--select` | `List[str]` | Comma-separated fields to select and show in output. Available: ['id', 'created', 'updated', 'name', 'path', 'broker_id'] | `['created', 'id', 'name', 'path']` |
| `--json` | `bool` | Output the result as JSON | `False` |

#### `ptc secrets info`

Show info about a secret on the cluster

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name_or_id` | `Union[str, UUID]` | Name or ID of the secret |  |
| `cluster_id` | `UUID` | ID of the cluster to search for secret name (or the last cluster if not set) | `None` |
| `--select` | `List[str]` | Comma-separated fields to select and show in output. Available: ['id', 'created', 'updated', 'name', 'path', 'broker_id'] | `None` |
| `--json` | `bool` | Output the result as JSON | `False` |

#### `ptc secrets create`

Create a named pointer to a secret on the cluster

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name` | `str` | Name of the secret name |  |
| `--secrets-path` | `str` | / separated key prefix to save secrets to | `'/'` |
| `--exists-ok` | `bool` | Don't raise an error if it exists | `False` |
| `_extra` | `List[str]` |  |  |

#### `ptc secrets delete`

Delete a secret by name or ID

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name_or_id` | `Union[str, UUID]` | Name or ID of the secret |  |
| `cluster_id` | `UUID` | ID of the cluster to search for secret name (or the last cluster if not set) | `None` |

### `ptc tasks`

Interact with annotation tasks on the cluster

#### `ptc tasks create`

Create a new task. The available task recipes are fetched from your cluster and are added as dynamic subcommands. You can see more details and available arguments by calling the subcommand with --help, e.g. create [name] --help

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `--exists-ok` | `bool` | Don't raise an error if it exists | `False` |
| `--no-start` | `bool` | Don't start {noun} after creation | `False` |
| `--help`, `-h` | `bool` | Show help message | `False` |
| `_extra` | `List[str]` |  | `[]` |

#### `ptc tasks list`

List the tasks on the cluster. By default, this includes their ID, name and current state, e.g. created or completed

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `--select` | `List[str]` | Comma-separated fields to select and show in output. Available: ['id', 'created', 'updated', 'project_id', 'broker_id', 'name', 'recipe_name', 'recipe_title', 'state', 'project_name', 'is_running', 'is_startable', 'is_stoppable', 'error', 'plan', 'job_type', 'cli_command'] | `['id', 'name', 'state', 'project_name']` |
| `--json` | `bool` | Output the result as JSON | `False` |

#### `ptc tasks info`

Print information about a task on the cluster

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name_or_id` | `Union[str, UUID]` | Name or ID of the task |  |
| `project_id` | `UUID` | ID of task's project (or the last project if not set) | `None` |
| `cluster_id` | `UUID` | ID of the cluster to search for task name (or the last cluster if not set) | `None` |
| `--select` | `List[str]` | Comma-separated fields to select and show in output. Available: ['id', 'created', 'updated', 'project_id', 'broker_id', 'name', 'recipe_name', 'recipe_title', 'state', 'project_name', 'is_running', 'is_startable', 'is_stoppable', 'error', 'plan', 'job_type', 'cli_command', 'nomad_index', 'last_execution_id', 'related_actions', 'url_logs', 'url', 'created_by_user'] | `None` |
| `--json` | `bool` | Output the result as JSON | `False` |

#### `ptc tasks logs`

Get logs for a task on the cluster

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name_or_id` | `str` | Name or ID of the tasks (or the last tasks if not set) | `None` |
| `project_id` | `UUID` | ID of tasks's project (or the last project if not set) | `None` |
| `cluster_id` | `UUID` | ID of the cluster to search for tasks name (or the last cluster if not set) | `None` |
| `--json` | `bool` | Output the result as JSON | `False` |

#### `ptc tasks start`

Start a task on the cluster

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name_or_id` | `str` | Name or ID of the task (or the last task if not set) | `None` |
| `project_id` | `UUID` | ID of task's project (or the last project if not set) | `None` |
| `cluster_id` | `UUID` | ID of the cluster to search for task name (or the last cluster if not set) | `None` |
| `--worker-class` | `str` | Worker class to launch the task on. Generally one of: ['medium', 'large', 'gpu'] | `None` |

#### `ptc tasks stop`

Stop a task on the cluster

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name_or_id` | `str` | Name or ID of the task (or the last task if not set) | `None` |
| `project_id` | `UUID` | ID of task's project (or the last project if not set) | `None` |
| `cluster_id` | `UUID` | ID of the cluster to search for task name (or the last cluster if not set) | `None` |

#### `ptc tasks delete`

Delete a task by name or ID

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name_or_id` | `Union[str, UUID]` | Name or ID of the task |  |
| `project_id` | `UUID` | ID of task's project (or the last project if not set) | `None` |
| `cluster_id` | `UUID` | ID of the cluster to search for task name (or the last cluster if not set) | `None` |

### `ptc publish`

Publish

#### `ptc publish code`

Upload and advertise a recipes package from your Python environment.

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `name_or_path` | `str` | Path or name of importable module with the recipes |  |
| `--python-version` | `str` | Which Python version to use for the remote environment | `'3.9'` |
| `--package-version` | `str` | Version identifier for the package | `None` |
| `--requirements`, `-r` | `Path` | Path to requirements file. prodigy and prodigy_teams_recipes_sdk and added automatically if missing | `None` |
| `--dep`, `-d` | `Path` | Path or name of importable module for dependencies to upload | `[]` |

#### `ptc publish data`

Transfer data to the cluster, and advertise it to Prodigy Teams. These steps can also be done separately. See `ptc files` to transfer data to the cluster without creating an Asset record for it, and `ptc assets create` to create an Asset without transfer.

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `src` | `Path` | File or directory to publish |  |
| `dest` | `str` | Destination path to copy the data to | `None` |
| `--name` | `str` | Name of the asset | `None` |
| `--version` | `str` | Version of the asset | `None` |
| `--kind` | `str` | Kind of the asset. Generally one of: ['Input', 'Model', 'Patterns] |  |
| `--loader` | `str` | Loader to convert data for Prodigy | `None` |
| `--meta` | `str` | Asset meta, formatted as a JSON string | `'{}'` |
| `--exists-ok` | `bool` | Don't raise an error if it exists | `False` |

### `ptc login`

Log in to your Prodigy Teams account. You normally don't need to call this manually. It will automatically authenticate when needed.

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `--no-cluster` | `bool` | Don't use a cluster | `False` |

### `ptc info`

Print information about the CLI

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `field` | `str` | Field to select and show in output | `None` |

### `ptc get-auth-token`

Return an auth token for the current user

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `token_type` | `str` | The token type | `None` |

### `ptc export`

Save the state of the current app JSON file. If an assets directory is provided, assets will be downloaded and referenced in the JSON accordingly.

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `output` | `Path` | JSON output path for data |  |
| `assets_dir` | `Path` | Local directory to download assets to | `None` |
| `--include` | `str` | Comma-separated items to include | `['tasks', 'actions', 'assets', 'datasets', 'paths']` |

### `ptc import`

Populate Prodigy Teams with data for projects, tasks, actions, assets and paths.

| Argument | Type | Description | Default |
| --- | --- | --- | --- |
| `data` | `Path` | JSON file to import |  |
| `--strict`, `-S` | `bool` | Error if items already exist and don't skip or overwrite anything | `False` |