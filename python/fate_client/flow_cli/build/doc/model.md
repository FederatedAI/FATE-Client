## model
Model Operations
### export
Export the model to a file.
```bash
flow model export [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| model_id | `-mid` | `--model-id` | yes | str | Model ID |
| model_version | `-mv` | `--model-version` | yes | str | Model version |
| party_id | `-p` | `--party-id` | yes | str | Site ID |
| role | `-r` | `--role` | no | str | Role of the participant: guest/host/arbiter/local |
| path | `-o` | `--path` | yes | path | Directory or file path on the client |

**Usage**
```bash
flow model export --model-id xxx --model-version xxx -p 9999 -r guest -o ./model/
```

### import
Import the model to storage engine.
```bash
flow model import [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| model_id | `-mid` | `--model-id` | yes | str | Model ID |
| model_version | `-mv` | `--model-version` | yes | str | Model version |
| path | `-i` | `--path` | yes | path | Directory or file path on the client |

**Usage**
```bash
flow model import --model-id xxx --model-version xxx -i $input_path
```

### delete
Delete Models Based on Conditions
```bash
flow model delete [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| model_id | `-mid` | `--model-id` | yes | str | Model ID |
| model_version | `-mv` | `--model-version` | yes | str | Model version |
| role | `-r` | `--role` | no | str | Role of the participant: guest/host/arbiter/local |
| party_id | `-p` | `--party-id` | no | str | Site ID |
| task_name | `-tn` | `--task-name` | no | str | Task name |
| output_key | - | `--output-key` | no | str | Primary key for output data or model of the task |

**Usage**
```bash
flow model delete --model-id xxx  --model-version xxx
```

