## output
Task output Operations
### query-metric-key
Query metric key
```bash
flow output query-metric-key [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| job_id | `-j` | `--job-id` | yes | str | Job ID |
| role | `-r` | `--role` | no | str | Role of the participant: guest/host/arbiter/local |
| party_id | `-p` | `--party-id` | yes | str | Site ID |
| task_name | `-tn` | `--task-name` | yes | str | Task name |

**Usage**
```bash
flow output query-metric-key -j xxx -r guest -p 9999 -tn lr_0
```

### query-metric
Query metric
```bash
flow output query-metric [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| job_id | `-j` | `--job-id` | yes | str | Job ID |
| role | `-r` | `--role` | no | str | Role of the participant: guest/host/arbiter/local |
| party_id | `-p` | `--party-id` | yes | str | Site ID |
| task_name | `-tn` | `--task-name` | yes | str | Task name |

**Usage**
```bash
flow output query-metric -j xxx -r guest -p 9999 -tn lr_0
```

### delete-metric
Delete metric
```bash
flow output delete-metric [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| job_id | `-j` | `--job-id` | yes | str | Job ID |
| role | `-r` | `--role` | no | str | Role of the participant: guest/host/arbiter/local |
| party_id | `-p` | `--party-id` | yes | str | Site ID |
| task_name | `-tn` | `--task-name` | yes | str | Task name |

**Usage**
```bash
flow output delete-metric -j xxx -r guest -p 9999 -tn lr_0
```

### query-model
Query model
```bash
flow output query-model [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| job_id | `-j` | `--job-id` | yes | str | Job ID |
| role | `-r` | `--role` | no | str | Role of the participant: guest/host/arbiter/local |
| party_id | `-p` | `--party-id` | yes | str | Site ID |
| task_name | `-tn` | `--task-name` | yes | str | Task name |

**Usage**
```bash
flow output query-model -j xxx -r guest -p 9999 -tn lr_0
```

### download-model
Download model
```bash
flow output download-model [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| job_id | `-j` | `--job-id` | yes | str | Job ID |
| role | `-r` | `--role` | no | str | Role of the participant: guest/host/arbiter/local |
| party_id | `-p` | `--party-id` | yes | str | Site ID |
| task_name | `-tn` | `--task-name` | yes | str | Task name |
| path | `-o` | `--path` | yes | path | Directory or file path on the client |

**Usage**
```bash
flow output download-model -j $JOB_ID -r guest -p 9999 -tn lr_0 -o /data/project/xxx
```

### delete-model
Delete Model
```bash
flow output delete-model [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| job_id | `-j` | `--job-id` | yes | str | Job ID |
| role | `-r` | `--role` | no | str | Role of the participant: guest/host/arbiter/local |
| party_id | `-p` | `--party-id` | yes | str | Site ID |
| task_name | `-tn` | `--task-name` | yes | str | Task name |

**Usage**
```bash
flow output delete-model -j $JOB_ID -r guest -p 9999 -tn lr_0
```

### download-data
Download Data
```bash
flow output download-data [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| job_id | `-j` | `--job-id` | yes | str | Job ID |
| role | `-r` | `--role` | no | str | Role of the participant: guest/host/arbiter/local |
| party_id | `-p` | `--party-id` | yes | str | Site ID |
| task_name | `-tn` | `--task-name` | yes | str | Task name |
| path | `-o` | `--path` | yes | path | Directory or file path on the client |

**Usage**
```bash
flow output download-data -j xxx -r guest -p 9999 -tn lr_0 -o /data/project/xx
```

### query-data-table
Query output data table info
```bash
flow output query-data-table [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| job_id | `-j` | `--job-id` | yes | str | Job ID |
| role | `-r` | `--role` | no | str | Role of the participant: guest/host/arbiter/local |
| party_id | `-p` | `--party-id` | yes | str | Site ID |
| task_name | `-tn` | `--task-name` | yes | str | Task name |

**Usage**
```bash
flow output query-data-table -j xxx -r guest -p 9999 -tn lr_0
```

### display-data
Display Data
```bash
flow output display-data [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| job_id | `-j` | `--job-id` | yes | str | Job ID |
| role | `-r` | `--role` | no | str | Role of the participant: guest/host/arbiter/local |
| party_id | `-p` | `--party-id` | yes | str | Site ID |
| task_name | `-tn` | `--task-name` | yes | str | Task name |

**Usage**
```bash
flow output display-data -j xxx -r guest -p 9999 -tn lr_0
```

