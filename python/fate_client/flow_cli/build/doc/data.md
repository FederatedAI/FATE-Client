## data
Provides numbers of data operational commands, including upload, download, transformer and etc. For more details, please check out the help text.
### upload
Upload data to storage engine.
```bash
flow data upload [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| conf_path | `-c` | `--conf-path` | yes | PATH | Configuration file path |

**Usage**
```bash
flow data upload -c examples/upload/upload_guest.json
```

### download-component
Asynchronously downloading data through download component.
```bash
flow data download-component [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| name | `-n` | `--name` | yes | TEXT | Name of the data table |
| namespace | `-ns` | `--namespace` | yes | TEXT | Namespace of the data table |
| path | `-o` | `--path` | yes | PATH | Directory or file path on the client |

**Usage**
```bash
flow data download-component --name 1bfaa4e6-4317-11ee-be20-16b977118319 --namespace upload -o /data/xxx
```

### transformer
Converting Data Table to DataFrame.
```bash
flow data transformer [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| conf_path | `-c` | `--conf-path` | yes | PATH | Configuration file path |

**Usage**
```bash
flow data transformer -c examples/transformer/transformer_guest.json
```

### download
Synchronous Data Download.
```bash
flow data download [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| name | `-n` | `--name` | yes | TEXT | Name of the data table |
| namespace | `-ns` | `--namespace` | yes | TEXT | Namespace of the data table |
| path | `-o` | `--path` | yes | PATH | Directory or file path on the client |

**Usage**
```bash
flow data download --name 1bfaa4e6-4317-11ee-be20-16b977118319 --namespace upload -o /data/xxx
```

