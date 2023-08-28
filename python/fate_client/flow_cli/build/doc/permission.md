## permission
Permission Operations
### grant
Grant permission
```bash
flow permission grant [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| app_id | - | `--app-id` | yes | TEXT | App ID for the client |
| role | `-r` | `--role` | yes | TEXT | Permission name |
**Usage**
```bash
flow permission grant --app-id xxx  -r xxx
```

### delete
Delete permission
```bash
flow permission delete [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| app_id | - | `--app-id` | yes | TEXT | App ID for the client |
| role | `-r` | `--role` | yes | TEXT | Permission name |
**Usage**
```bash
flow permission delete --app-id xxx --role client
```

### query
Query permission
```bash
flow permission query [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| app_id | - | `--app-id` | yes | TEXT | App ID for the client |
**Usage**
```bash
flow permission query --app-id xxx
```

### grant-resource
Granting Permissions to components, Datasets, etc.
```bash
flow permission grant-resource [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| conf_path | `-c` | `--conf-path` | yes | PATH | Configuration file path |
**Usage**
```bash
flow permission grant-resource -c examples/permission/grant.json
```

### delete-resource
Delete Permissions of components, Datasets, etc.
```bash
flow permission delete-resource [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| conf_path | `-c` | `--conf-path` | yes | PATH | Configuration file path |
**Usage**
```bash
flow permission delete-resource -c examples/permission/delete.json
```

### query-resource
Query Permissions of components, Datasets, etc.
```bash
flow permission query-resource [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| party_id | `-p` | `--party-id` | yes | TEXT | Site ID |
**Usage**
```bash

```

