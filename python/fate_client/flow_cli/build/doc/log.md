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
| log_type | - | `--log-type` | yes | TEXT | Log level or type |
| job_id | `-j` | `--job-id` | yes | TEXT | Job ID |
| role | `-r` | `--role` | no | TEXT | Role of the participant: guest/host/arbiter/local |
| party_id | `-p` | `--party-id` | no | TEXT | Site ID |
| instance_id | - | `--instance-id` | no | TEXT | Instance ID of the FATE Flow service |

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
| log_type | - | `--log-type` | yes | TEXT | Log level or type |
| job_id | `-j` | `--job-id` | yes | TEXT | Job ID |
| role | `-r` | `--role` | no | TEXT | Role of the participant: guest/host/arbiter/local |
| party_id | `-p` | `--party-id` | no | TEXT | Site ID |
| task_name | `-tn` | `--task-name` | no | TEXT | Task name |
| instance_id | - | `--instance-id` | no | TEXT | Instance ID of the FATE Flow service |

**Usage**
```bash
flow log query -j 202308251856000656610 -r guest -p 9999  --log-type schedule_info
```

