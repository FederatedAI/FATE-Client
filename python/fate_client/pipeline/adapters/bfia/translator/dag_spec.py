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
from typing import Optional, Dict, List

from pydantic import BaseModel


class InitiatorSpec(BaseModel):
    role: str
    node_id: str


class RoleSpec(BaseModel):
    guest: Optional[List[str]]
    host: Optional[List[str]]
    arbiter: Optional[List[str]]
    local: Optional[List[str]]


class JobCommonSpec(BaseModel):
    sync_type: Optional[str] = "poll"


class JobParamsSpec(BaseModel):
    common: Optional[JobCommonSpec]
    guest: Optional[Dict]
    host: Optional[Dict]
    arbiter: Optional[Dict]


class TaskParamsSpec(BaseModel):
    common: Optional[Dict]
    guest: Optional[Dict]
    host: Optional[Dict]
    arbiter: Optional[Dict]


class ConfSpec(BaseModel):
    initiator: InitiatorSpec
    role: RoleSpec
    job_params: JobParamsSpec
    task_params: TaskParamsSpec
    version: str


class DataSpec(BaseModel):
    key: str
    type: str


class DagComponentSpec(BaseModel):
    name: str
    componentName: str
    provider: str
    version: str
    input: Optional[List[DataSpec]] = []
    output: Optional[List[DataSpec]] = []


class DagSpec(BaseModel):
    components: List[DagComponentSpec]
    version: str


class BFIADagSpec(BaseModel):
    flow_id: Optional[str]
    config: ConfSpec
    dag: DagSpec
    old_job_id: Optional[str]


class DagSchemaSpec(BaseModel):
    dag: BFIADagSpec
    schema_version: str
    kind: str
