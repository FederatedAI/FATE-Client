## task
Provides numbers of task operational commands, including list and query. For more details, please check out the help text.
### query
Querying Tasks by Filtering Conditions.
```bash
flow task query [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| job_id | `-j` | `--job-id` | no | str | Job ID |
| role | `-r` | `--role` | no | str | Role of the participant: guest/host/arbiter/local |
| party_id | `-p` | `--party-id` | no | str | Site ID |
| task_name | `-tn` | `--task-name` | no | str | Task name |
| status | `-s` | `--status` | no | str | Status of the job or task |
| task_id | `-tid` | `--task-id` | no | str | Task ID |
| task_version | `-tv` | `--task-version` | no | str | Task version |

**Usage**
```bash
flow task query -j xxx -r guest -p 9999 -tn xxx
```

### list
Fetching Task List by Filtering Conditions.
```bash
flow task list [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| job_id | `-j` | `--job-id` | no | str | Job ID |
| role | `-r` | `--role` | no | str | Role of the participant: guest/host/arbiter/local |
| party_id | `-p` | `--party-id` | no | str | Site ID |
| task_name | `-tn` | `--task-name` | no | str | Task name |
| limit | `-l` | `--limit` | no | integer | Limit of rows or entries |

**Usage**
```bash
flow task list -j xxx -r guest -p 9999
```

