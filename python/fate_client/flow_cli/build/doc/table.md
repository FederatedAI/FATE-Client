## table
Data Table Operations, such as Querying and Deleting, and more
### query
Query data table.
```bash
flow table query [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| namespace | `-ns` | `--namespace` | yes | str | Namespace of the data table |
| name | `-n` | `--name` | yes | str | Name of the data table |
| display | `-d` | `--display` | no | str | Whether to return preview data |

**Usage**
```bash
flow table query --name xxx --namespace xxx
```

### delete
Delete data table.
```bash
flow table delete [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| namespace | `-ns` | `--namespace` | yes | str | Namespace of the data table |
| name | `-n` | `--name` | yes | str | Name of the data table |

**Usage**
```bash
flow table delete --name xxx --namespace xxx
```

### bind
Bind data table.
```bash
flow table bind [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| namespace | `-ns` | `--namespace` | yes | str | Namespace of the data table |
| name | `-n` | `--name` | yes | str | Name of the data table |
| path | `-o` | `--path` | yes | path | Directory or file path on the client |

**Usage**
```bash
flow table bind --name xxx --namespace xxx -o /data/xxx
```

