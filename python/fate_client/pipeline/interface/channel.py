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
import abc
from typing import Dict, Optional, Union, TypeVar
from ..conf.types import ArtifactSourceType
from ..entity.dag_structures import DataWarehouseChannelSpec, ModelWarehouseChannelSpec, RuntimeTaskOutputChannelSpec


class TaskOutputArtifactChannel(abc.ABC):
    def __init__(
            self,
            name: str,
            channel_type: Union[str, Dict],
            task_name: Optional[str] = None,
    ):
        self.name = name
        self.channel_type = channel_type
        self.task_name = task_name or None
        self.source = ArtifactSourceType.TASK_OUTPUT_ARTIFACT

    def get_spec(self, **kwargs):
        roles = kwargs.get("roles", None) if kwargs else None
        return RuntimeTaskOutputChannelSpec(
            producer_task=self.task_name,
            output_artifact_key=self.name,
            roles=roles
        )

    def __str__(self):
        return "{" + f"channel:task={self.task_name};" \
                     f"name={self.name};" \
                     f"type={self.channel_type};" \
                     f"source={self.source};" + "}"

    def __repr__(self):
        return str(self)


class DataWarehouseChannel(abc.ABC):
    def __init__(
            self,
            name: str,
            namespace: str,
            job_id: str = None,
            producer_task: str = None,
            output_artifact_key: str = None,
    ):
        self.name = name
        self.namespace = namespace
        self.job_id = job_id
        self.producer_task = producer_task
        self.output_artifact_key = output_artifact_key
        self.source = ArtifactSourceType.DATA_WAREHOUSE

    def get_spec(self, **kwargs):
        roles = kwargs.get("roles", None) if kwargs else None
        return DataWarehouseChannelSpec(
            name=self.name,
            namespace=self.namespace,
            job_id=self.job_id,
            producer_task=self.producer_task,
            output_artifact_key=self.output_artifact_key,
            roles=roles
        )

    def __str__(self):
        return "{" + f"channel:name={self.name};" \
                     f"namespace={self.namespace};" \
                     f"job_id={self.job_id};" \
                     f"producer_task={self.producer_task};" \
                     f"output_artifact_key={self.output_artifact_key};" \
                     f"source={self.source};" + "}"

    def __repr__(self):
        return str(self)


class ModelWarehouseChannel(abc.ABC):
    def __init__(
        self,
        model_id: str,
        model_version: str,
        producer_task: str,
        output_artifact_key: str,
        roles: list
    ):
        self.model_id = model_id
        self.model_version = model_version
        self.producer_task = producer_task
        self.output_artifact_key = output_artifact_key
        self.roles = roles
        self.source = ArtifactSourceType.MODEL_WAREHOUSE

    def get_spec(self, **kwargs):
        return ModelWarehouseChannelSpec(
            model_id=self.model_id,
            model_version=self.model_version,
            producer_task=self.producer_task,
            output_artifact_key=self.output_artifact_key
        )

    def __str__(self):
        return "{" + f"channel:model_id={self.model_id};" \
                     f"model_version={self.model_version};" \
                     f"producer_task={self.producer_task};" \
                     f"output_artifact_key={self.output_artifact_key};" \
                     f"roles={self.roles};" \
                     f"source={self.source};" + "}"

    def __repr__(self):
        return str(self)


ArtifactType = TypeVar("ArtifactType",
                       TaskOutputArtifactChannel,
                       DataWarehouseChannel,
                       ModelWarehouseChannel)
