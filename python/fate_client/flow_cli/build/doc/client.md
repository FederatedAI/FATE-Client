## client
Client Operations
### create-client
Create a client
```bash
flow client create-client [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| app_name | - | `--app-name` | yes | TEXT | App name for the client |

**Usage**
```bash
flow client create-client --app-name xxx
```

### delete-client
Delete a client
```bash
flow client delete-client [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| app_id | - | `--app-id` | yes | TEXT | App ID for the client |

**Usage**
```bash
flow client delete-client --app-id xxx
```

### query-client
Querying Client Information by Filtering Conditions
```bash
flow client query-client [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| app_id | - | `--app-id` | no | TEXT | App ID for the client |
| app_name | - | `--app-name` | no | TEXT | App name for the client |

**Usage**
```bash
flow client query-client  --app-id xxx --app-name xxx
```

### create-site
Create partner site
```bash
flow client create-site [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| party_id | `-p` | `--party-id` | yes | TEXT | Site ID |

**Usage**
```bash
flow client create-site -p xxx
```

### delete-site
Delete partner site
```bash
flow client delete-site [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| party_id | `-p` | `--party-id` | yes | TEXT | Site ID |

**Usage**
```bash
flow client delete-site -p xxx
```

### query-site
Query partner site
```bash
flow client query-site [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| party_id | `-p` | `--party-id` | yes | TEXT | Site ID |

**Usage**
```bash
flow client query-site -p xxx
```

### create-partner
Establishing Partnership with a Site
```bash
flow client create-partner [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| party_id | `-p` | `--party-id` | yes | TEXT | Site ID |
| app_id | - | `--app-id` | yes | TEXT | App ID for the client |
| app_token | - | `--app-token` | yes | TEXT | App token for the site |

**Usage**
```bash
flow create create-partner -p xxx
```

### delete-partner
Disassociating Partnership with a Site.
```bash
flow client delete-partner [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| party_id | `-p` | `--party-id` | yes | TEXT | Site ID |

**Usage**
```bash
flow client delete-partner -p xxx
```

### query-partner
Querying Sites with Established Partnerships.
```bash
flow client query-partner [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| party_id | `-p` | `--party-id` | no | TEXT | Site ID |

**Usage**
```bash
flow client query-partner -p xxx
```

