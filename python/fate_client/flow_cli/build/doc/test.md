## test
fate test
### toy
Connectivity test.
```bash
flow test toy [OPTIONS]
```
**Options**

| parameters | short-format | long-format | required | type | description |
| :-------- |:-----|:-------------| :--- | :----- |------|
| guest_party_id | `-gid` | `--guest-party-id` | yes | str | Site ID of the guest |
| host_party_id | `-hid` | `--host-party-id` | yes | str | Site ID of the host |
| timeout | `-t` | `--timeout` | no | integer | Timeout limit |

**Usage**
```bash
flow test toy -gid 9999 -hid 10000
```

