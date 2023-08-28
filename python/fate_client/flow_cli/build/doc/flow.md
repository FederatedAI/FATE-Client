## flow
FATE Flow client
### init
Flow CLI Init Command. provide ip and port of a valid fate flow server.If the server enables client authentication, you need to configure app-id and app-token
```bash
flow init [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| ip | - | `--ip` | no | TEXT | Fate flow server ip address. |
| port | - | `--port` | no | INTEGER | Fate flow server port. |
| app_id | - | `--app-id` | no | TEXT | APP key for sign requests. |
| app_token | - | `--app-token` | no | TEXT | Secret key for sign requests. |

**Usage**
```bash
flow init --ip 127.0.0.1 --port 9380
```

### version
Get fate flow client version
```bash
flow version [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|

**Usage**
```bash
flow version
```

