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
from pydantic import BaseModel
from typing import Optional, Literal, List, Union, Dict, Any, TypeVar


class PartySpec(BaseModel):
    role: Union[Literal["guest", "host", "arbiter", "local"]]
    party_id: List[str]


class RuntimeTaskOutputChannelSpec(BaseModel):
    producer_task: str
    output_artifact_key: str
    output_artifact_type_alias: Optional[str]
    parties: Optional[List[PartySpec]]

    class Config:
        extra = "forbid"


class DataWarehouseChannelSpec(BaseModel):
    namespace: Optional[str]
    name: Optional[str]
    dataset_id: Optional[str]
    parties: Optional[List[PartySpec]]

    class Config:
        extra = "forbid"


class ModelWarehouseChannelSpec(BaseModel):
    model_id: Optional[str]
    model_version: Optional[str]
    producer_task: str
    output_artifact_key: str
    parties: Optional[List[PartySpec]]

    class Config:
        extra = "forbid"


InputArtifactSpec = TypeVar("InputArtifactSpec",
                            RuntimeTaskOutputChannelSpec,
                            ModelWarehouseChannelSpec,
                            DataWarehouseChannelSpec)


class RuntimeInputArtifacts(BaseModel):
    data: Optional[Dict[str, Dict[str, Union[List[InputArtifactSpec], InputArtifactSpec]]]]
    model: Optional[Dict[str, Dict[str, Union[List[InputArtifactSpec], InputArtifactSpec]]]]


class ModelWarehouseConfSpec(BaseModel):
    model_id: Optional[str]
    model_version: Optional[str]


class OutputArtifactSpec(BaseModel):
    output_artifact_key_alias: str
    output_artifact_type_alias: str
    parties: Optional[List[PartySpec]]


class OutputArtifacts(BaseModel):
    data: Optional[Dict[str, Union[OutputArtifactSpec, List[OutputArtifactSpec]]]]
    model: Optional[Dict[str, Union[OutputArtifactSpec, List[OutputArtifactSpec]]]]
    metric: Optional[Dict[str, Union[OutputArtifactSpec, List[OutputArtifactSpec]]]]


class TaskSpec(BaseModel):
    component_ref: str
    dependent_tasks: Optional[List[str]]
    parameters: Optional[Dict[Any, Any]]
    inputs: Optional[RuntimeInputArtifacts]
    outputs: Optional[OutputArtifacts]
    parties: Optional[List[PartySpec]]
    conf: Optional[Dict[Any, Any]]
    stage: Optional[Union[Literal["train", "predict", "default", "cross_validation"]]]


class PartyTaskRefSpec(BaseModel):
    parameters: Optional[Dict[Any, Any]]
    conf: Optional[Dict] = {}


class PartyTaskSpec(BaseModel):
    parties: Optional[List[PartySpec]]
    tasks: Optional[Dict[str, PartyTaskRefSpec]]
    conf: Optional[dict] = {}


class TaskConfSpec(BaseModel):
    engine_run: Optional[Dict]
    provider: Optional[str]
    timeout: Optional[int]
    launcher_name: Optional[str] = "default"


class EngineRunSpec(BaseModel):
    name: str
    conf: Optional[Dict]


class InheritConfSpec(BaseModel):
    job_id: str
    task_list: List[str]


class JobConfSpec(BaseModel):
    priority: Optional[int]
    scheduler_party_id: Optional[str]
    inheritance: Optional[InheritConfSpec]
    task_parallelism: Optional[int]
    cores: Optional[int]
    computing_partitions: Optional[int]
    sync_type: Optional[Union[Literal["poll", "callback"]]]
    federated_status_collect_type: Optional[str]
    auto_retries: Optional[int]
    model_warehouse: Optional[ModelWarehouseConfSpec]
    model_id: Optional[str]
    model_version: Optional[str]
    task: Optional[TaskConfSpec]
    engine: Optional[EngineRunSpec]

    extra: Optional[Dict[Any, Any]]


class DAGSpec(BaseModel):
    parties: List[PartySpec]
    conf: Optional[JobConfSpec]
    stage: Optional[Union[Literal["train", "predict", "default", "cross_validation"]]]
    tasks: Dict[str, TaskSpec]
    party_tasks: Optional[Dict[str, PartyTaskSpec]]


class DAGSchema(BaseModel):
    dag: DAGSpec
    schema_version: str
    kind: str = "fate"
