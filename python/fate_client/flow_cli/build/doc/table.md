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
| namespace | `-ns` | `--namespace` | yes | TEXT | Namespace of the data table |
| name | `-n` | `--name` | yes | TEXT | Name of the data table |
| display | `-d` | `--display` | no | TEXT | Whether to return preview data |
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
| namespace | `-ns` | `--namespace` | yes | TEXT | Namespace of the data table |
| name | `-n` | `--name` | yes | TEXT | Name of the data table |
**Usage**
```bash
flow table delete --name xxx --namespace xxx
```

