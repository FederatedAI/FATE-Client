## log
Operations related to job logs.
### count
Fetching the total number of lines in the log.
```bash
flow log count [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| log_type | - | `--log-type` | yes | str | Log level or type |
| job_id | `-j` | `--job-id` | yes | str | Job ID |
| role | `-r` | `--role` | no | str | Role of the participant: guest/host/arbiter/local |
| party_id | `-p` | `--party-id` | no | str | Site ID |
| instance_id | - | `--instance-id` | no | str | Instance ID of the FATE Flow service |

**Usage**
```bash
flow log count -j 202308211557455662860 -r guest -p 9999 --log-type schedule_info
```

### query

```bash
flow log query [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| log_type | - | `--log-type` | yes | str | Log level or type |
| job_id | `-j` | `--job-id` | yes | str | Job ID |
| role | `-r` | `--role` | no | str | Role of the participant: guest/host/arbiter/local |
| party_id | `-p` | `--party-id` | no | str | Site ID |
| task_name | `-tn` | `--task-name` | no | str | Task name |
| instance_id | - | `--instance-id` | no | str | Instance ID of the FATE Flow service |

**Usage**
```bash
flow log query -j 202308251856000656610 -r guest -p 9999  --log-type schedule_info
```

