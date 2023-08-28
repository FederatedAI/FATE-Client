## provider
Provider Operations
### register
register provider
```bash
flow provider register [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| conf_path | `-c` | `--conf-path` | yes | PATH | Configuration file path |
**Usage**
```bash
flow provider register -c examples/provider/register.json
```

### query
Filtering Providers Based on Conditions
```bash
flow provider query [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| name | `-n` | `--name` | no | TEXT | Name of the data table |
| device | - | `--device` | no | TEXT | Component running mode |
| version | - | `--version` | no | TEXT | Component version |
| provider_name | - | `--provider-name` | no | TEXT | Component provider name |
**Usage**
```bash
flow provider register --name fate
```

### delete
Delete Providers Based on Filtering Conditions.
```bash
flow provider delete [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| name | `-n` | `--name` | no | TEXT | Name of the data table |
| device | - | `--device` | no | TEXT | Component running mode |
| version | - | `--version` | no | TEXT | Component version |
| provider_name | - | `--provider-name` | no | TEXT | Component provider name |
**Usage**
```bash
flow provider delete -n xxx
```

