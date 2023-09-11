## job
Provides numbers of job operational commands, including submit, stop, query etc. For more details, please check out the help text.
### submit
Submit and create a job.
```bash
flow job submit [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| conf_path | `-c` | `--conf-path` | yes | path | Configuration file path |

**Usage**
```bash
flow job submit -c examples/lr/train_lr.yaml
```

### query
Querying jobs through filtering conditions.
```bash
flow job query [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| job_id | `-j` | `--job-id` | no | str | Job ID |
| role | `-r` | `--role` | no | str | Role of the participant: guest/host/arbiter/local |
| party_id | `-p` | `--party-id` | no | str | Site ID |
| status | `-s` | `--status` | no | str | Status of the job or task |

**Usage**
```bash
flow job query -j 202308211557455662860 -r guest -p 9999 -s running
```

### add-notes
Add notes for job.
```bash
flow job add-notes [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| job_id | `-j` | `--job-id` | yes | str | Job ID |
| role | `-r` | `--role` | yes | str | Role of the participant: guest/host/arbiter/local |
| party_id | `-p` | `--party-id` | yes | str | Site ID |
| notes | - | `--notes` | yes | str | Tags and customizable information for job |

**Usage**
```bash
flow job add-notes -j 202308211557455662860 -r guest -p 9999 --notes "this is a test"
```

### stop
Stopping a running job.
```bash
flow job stop [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| job_id | `-j` | `--job-id` | yes | str | Job ID |

**Usage**
```bash
flow job stop -j 202308211557455662860
```

### rerun
Rerunning a failed job.
```bash
flow job rerun [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| job_id | `-j` | `--job-id` | yes | str | Job ID |

**Usage**
```bash
flow job rerun -j 202308211557455662860
```

### list
Fetching a list of jobs based on conditions.
```bash
flow job list [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| job_id | `-j` | `--job-id` | no | str | Job ID |
| role | `-r` | `--role` | no | str | Role of the participant: guest/host/arbiter/local |
| party_id | `-p` | `--party-id` | no | str | Site ID |
| status | `-s` | `--status` | no | str | Status of the job or task |
| limit | `-l` | `--limit` | no | integer | Limit of rows or entries |

**Usage**
```bash
flow job list -j 202308211557455662860 -r guest -p 9999
```

### download-log
Downloading job logs.
```bash
flow job download-log [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| job_id | `-j` | `--job-id` | yes | str | Job ID |
| path | `-o` | `--path` | yes | path | Directory or file path on the client |

**Usage**
```bash
flow job download-log -j 202308211557455662860 -o /data/project/examples/
```

### clean-queue

```bash
flow job clean-queue [OPTIONS]
```

**Usage**
```bash
flow job clean-queue
```

### clean
Cleaning up job output data.
```bash
flow job clean [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| job_id | `-j` | `--job-id` | yes | str | Job ID |

**Usage**
```bash
flow job clean -j 202308211557455662860
```

### dependency
Dependency relationships between tasks within a job.
```bash
flow job dependency [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| job_id | `-j` | `--job-id` | yes | str | Job ID |
| role | `-r` | `--role` | yes | str | Role of the participant: guest/host/arbiter/local |
| party_id | `-p` | `--party-id` | yes | str | Site ID |

**Usage**
```bash
flow job dependency -j 202308211557455662860 -r guest -p 9999
```

