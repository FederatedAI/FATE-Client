#
#  Copyright 2019 The FATE Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
import click

from fate_client.flow_cli.utils.args_desc import CONF_PATH_DESC, LIMIT_DESC, JOB_ID_DESC, ROLE_DESC, \
    PERMISSION_ROLE_DESC, PARTY_ID_DESC, APP_ID_DESC, APP_NAME_DESC, SITE_APP_TOKEN_DESC, GUEST_PARTY_ID_DESC, \
    HOST_PARTY_ID_DESC, TASK_NAME_DESC, TASK_ID_DESC, TASK_VERSION_DESC, STATUS_DESC, CLIENT_PATH_DESC, NAME_DESC, \
    NAMESPACE_DESC, DISPLAY_DESC, MODEL_ID_DESC, MODEL_VERSION_DESC, SERVICE_NAME_DESC, SERVER_NAME_DESC, TIMEOUT_DESC, \
    TASK_CORES_DESC, LOG_TYPE_DESC, INSTANCE_ID_DESC, OUTPUT_KEY_DESC, DEVICE_DESC, VERSION_DESC, URI_DESC, METHOD_DESC, \
    PARAMS_DESC, DATA_DESC, PROTOCOL_DESC, PROVIDER_NAME_DESC, HOST_DESC, PORT_DESC, NODES_DESC, TYPES_DESC, \
    ARBITER_PARTY_ID_DESC

role_ide_list = ["guest", "host", "arbiter", "local"]
role_choices_list = ["site", "client", "super_client"]
status_choices_list = ["success", "failed", "running", "waiting", "timeout", "canceled", "partial", "deleted"]

CONF_PATH = click.option("-c", "--conf-path", type=click.Path(exists=True), required=True, help=CONF_PATH_DESC)
LIMIT = click.option("-l", "--limit", type=click.INT, default=10, help=LIMIT_DESC)
JOBID = click.option("-j", "--job-id", type=click.STRING, help=JOB_ID_DESC)
JOBID_REQUIRED = click.option("-j", "--job-id", type=click.STRING, required=True, help=JOB_ID_DESC)
ROLE_IDE = click.option("-r", "--role", type=click.Choice(role_ide_list), metavar="TEXT", help=ROLE_DESC)
ROLE_IDE_REQUIRED = click.option("-r", "--role", type=click.Choice(role_ide_list), required=True, metavar="TEXT", help=ROLE_DESC)
ROLE_REQUIRED = click.option("-r", "--role", type=click.Choice(role_choices_list), required=True, metavar="TEXT", help=PERMISSION_ROLE_DESC)

PARTYID = click.option("-p", "--party-id", type=click.STRING, help=PARTY_ID_DESC)
PARTYID_REQUIRED = click.option("-p", "--party-id", type=click.STRING, required=True, help=PARTY_ID_DESC)
NOTES_REQUIRED = click.option("--notes", type=click.STRING, required=True, help=NODES_DESC)
APP_ID = click.option("--app-id", type=click.STRING, help=APP_ID_DESC)
APP_ID_REQUIRED = click.option("--app-id", type=click.STRING, required=True,help=APP_ID_DESC)
APP_NAME = click.option("--app-name", type=click.STRING, help=APP_NAME_DESC)
APP_NAME_REQUIRED = click.option("--app-name", type=click.STRING, required=True, help=APP_NAME_DESC)
APP_TOKEN = click.option("--app-token", type=click.STRING, help=SITE_APP_TOKEN_DESC)
APP_TOKEN_REQUIRED = click.option("--app-token", type=click.STRING, required=True, help=SITE_APP_TOKEN_DESC)
GUEST_PARTYID_REQUIRED = click.option(
    "-gid", "--guest-party-id", type=click.STRING, required=True, help=GUEST_PARTY_ID_DESC
)
HOST_PARTYID_REQUIRED = click.option(
    "-hid", "--host-party-id", type=click.STRING, required=True, help=HOST_PARTY_ID_DESC
)

ARBITER_PARTYID_REQUIRED = click.option(
    "-aid", "--arbiter-party-id", type=click.STRING, required=True, help=ARBITER_PARTY_ID_DESC
)
TASK_NAME = click.option("-tn", "--task-name", type=click.STRING, help=TASK_NAME_DESC)
TASK_NAME_REQUIRED = click.option("-tn", "--task-name", type=click.STRING, help=TASK_NAME_DESC, required=True,)
TASK_ID = click.option("-tid", "--task-id", type=click.STRING, help=TASK_ID_DESC)
TASK_ID_REQUIRED = click.option("-tid", "--task-id", type=click.STRING, help=TASK_ID_DESC, required=True,)
TASK_VERSION = click.option("-tv", "--task-version", type=click.STRING, help=TASK_VERSION_DESC)
STATUS = click.option("-s", "--status", type=click.Choice(status_choices_list), metavar="TEXT", help=STATUS_DESC)
OUTPUT_PATH = click.option("-o", "--output-path", type=click.Path(exists=False), help=CLIENT_PATH_DESC)
OUTPUT_PATH_REQUIRED = click.option("-o", "--output-path", type=click.Path(exists=False), required=True, help=CLIENT_PATH_DESC)
PATH = click.option("-o", "--path", type=click.Path(exists=False), help=CLIENT_PATH_DESC)
PATH_REQUIRED = click.option("-o", "--path", type=click.Path(exists=False), help=CLIENT_PATH_DESC, required=True)
INPUT_PATH_REQUIRED = click.option("-i", "--path", type=click.Path(exists=False), help=CLIENT_PATH_DESC, required=True)
NAME = click.option("-n", "--name", type=click.STRING, help=NAME_DESC)
NAME_REQUIRED = click.option("-n", "--name", type=click.STRING, help=NAME_DESC, required=True)
NAMESPACE = click.option("-ns", "--namespace", type=click.STRING, help=NAMESPACE_DESC)
NAMESPACE_REQUIRED = click.option("-ns", "--namespace", type=click.STRING, required=True, help=NAMESPACE_DESC)
DISPLAY = click.option("-d", "--display", type=click.STRING, required=False, help=DISPLAY_DESC)
MODEL_ID = click.option("-mid", "--model-id", type=click.STRING, help=MODEL_ID_DESC)
MODEL_ID_REQUIRED = click.option("-mid", "--model-id", type=click.STRING, required=True, help=MODEL_ID_DESC)
MODEL_VERSION = click.option("-mv", "--model-version", type=click.STRING, help=MODEL_VERSION_DESC)
MODEL_VERSION_REQUIRED = click.option("-mv", "--model-version", type=click.STRING, required=True, help=MODEL_VERSION_DESC)
SERVICE_NAME_REQUIRED = click.option("--service-name", type=click.STRING, required=True, help=SERVICE_NAME_DESC)
SERVER_NAME = click.option("--server-name", type=click.STRING, help=SERVER_NAME_DESC)
SERVER_NAME_REQUIRED = click.option("--server-name", type=click.STRING, required=True, help=SERVER_NAME_DESC)
TIMEOUT = click.option("-t", "--timeout", type=click.INT, default=300, help=TIMEOUT_DESC)
TASK_CORES = click.option("--task-cores", type=click.INT, default=2,help=TASK_CORES_DESC)

LOG_TYPE_REQUIRED = click.option("--log-type", type=click.STRING, required=True, help=LOG_TYPE_DESC)
INSTANCE_ID = click.option("--instance-id", type=click.STRING, help=INSTANCE_ID_DESC)
OUTPUT_KEY = click.option("--output-key", type=click.STRING, help=OUTPUT_KEY_DESC)
DEVICE = click.option("--device", type=click.STRING, help=DEVICE_DESC)
DEVICE_REQUIRED = click.option("--device", type=click.STRING, help=DEVICE_DESC, required=True)
VERSION = click.option("--version", type=click.STRING, help=VERSION_DESC)
VERSION_REQUIRED = click.option("--version", type=click.STRING, help=VERSION_DESC, required=True)
URI_REQUIRED = click.option("--uri", type=click.STRING, help=URI_DESC, required=True)
METHOD = click.option("--method", type=click.STRING, help=METHOD_DESC)
PARAMS = click.option("--params", type=click.STRING, help=PARAMS_DESC)
DATA = click.option("--data", type=click.STRING, help=DATA_DESC)
PROTOCOL = click.option("--protocol", type=click.STRING, help=PROTOCOL_DESC)
PROVIDER_NAME = click.option("--provider-name", type=click.STRING, help=PROVIDER_NAME_DESC)
HOST_REQUIRED = click.option("--host", type=click.STRING, help=HOST_DESC)
PORT_REQUIRED = click.option("--port", type=click.STRING, help=PORT_DESC)
