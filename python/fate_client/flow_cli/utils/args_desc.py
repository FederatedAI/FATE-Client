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

# job
CONF_PATH_DESC = "Configuration file path"
DAG_SCHEMA_DESC = "Definition and configuration of jobs, including the configuration of multiple tasks"
USER_NAME_DESC = "Username provided by the upper-level system"
JOB_ID_DESC = "Job ID"
ROLE_DESC = "Role of the participant: guest/host/arbiter/local"
STATUS_DESC = "Status of the job or task"
LIMIT_DESC = "Limit of rows or entries"
PAGE_DESC = "Page number"
DESCRIPTION_DESC = "Description information"
PARTNER_DESC = "Participant information"
ORDER_BY_DESC = "Field name for sorting"
ORDER_DESC = "Sorting order: asc/desc"
NODES_DESC = "Tags and customizable information for job"

# task
TASK_NAME_DESC = "Task name"
TASK_ID_DESC = "Task ID"
TASK_VERSION_DESC = "Task version"

# data
SERVER_FILE_PATH_DESC = "File path on the server"
SERVER_DIR_PATH_DESC = "Directory path on the server"
HEAD_DESC = "Whether the first row of the file is the data's head"
PARTITIONS_DESC = "Number of data partitions"
META_DESC = "Metadata of the data"
EXTEND_SID_DESC = "Whether to automatically fill a column as data row ID"
NAMESPACE_DESC = "Namespace of the data table"
NAME_DESC = "Name of the data table"
DATA_WAREHOUSE_DESC = "Data output, content like: {name: xxx, namespace: xxx}"
DROP_DESC = "Whether to destroy data if it already exists"
DOWNLOAD_HEADER_DESC = "Whether to download the data's head as the first row"
TYPES_DESC = "Down types:sync,async"

# output
FILTERS_DESC = "Filter conditions"
OUTPUT_KEY_DESC = "Primary key for output data or model of the task"

# table
DISPLAY_DESC = "Whether to return preview data"

# server
SERVER_NAME_DESC = "Server name"
SERVICE_NAME_DESC = "Service name"
HOST_DESC = "Host IP"
PORT_DESC = "Service port"
PROTOCOL_DESC = "Protocol: http/https"
URI_DESC = "Service path"
METHOD_DESC = "Request method: POST/GET, etc."
PARAMS_DESC = "Request header parameters"
DATA_DESC = "Request body parameters"
HEADERS_DESC = "Request headers"

# provider
PROVIDER_NAME_DESC = "Component provider name"
DEVICE_DESC = "Component running mode"
VERSION_DESC = "Component version"
COMPONENT_METADATA_DESC = "Detailed information about component registration"
PROVIDER_ALL_NAME_DESC = "Registered algorithm full name, provider + ':' + version + '@' + running mode, e.g., fate:2.0.0@local"

# permission
PERMISSION_APP_ID_DESC = "App ID"
PERMISSION_ROLE_DESC = "Permission name"
COMPONENT_DESC = "Component name"
DATASET_DESC = "List of datasets"

# log
LOG_TYPE_DESC = "Log level or type"
INSTANCE_ID_DESC = "Instance ID of the FATE Flow service"
BEGIN_DESC = "Starting line number"
END_DESC = "Ending line number"

# site
PARTY_ID_DESC = "Site ID"

# model
MODEL_ID_DESC = "Model ID"
MODEL_VERSION_DESC = "Model version"

# app
APP_NAME_DESC = "App name for the client"
APP_ID_DESC = "App ID for the client"
SITE_APP_ID_DESC = "App ID for the site"
SITE_APP_TOKEN_DESC = "App token for the site"


GUEST_PARTY_ID_DESC = "Site ID of the guest"
HOST_PARTY_ID_DESC = "Site ID of the host"
CLIENT_PATH_DESC = "Directory or file path on the client"
TIMEOUT_DESC = "Timeout limit"
TASK_CORES_DESC = "Task cores"
