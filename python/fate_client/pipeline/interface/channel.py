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
from typing import Dict, Optional, Union, TypeVar, List
from ..conf.types import ArtifactSourceType
from ..entity.dag_structures import (
    DataWarehouseChannelSpec,
    ModelWarehouseChannelSpec,
    RuntimeTaskOutputChannelSpec,
    PartySpec,
)


class TaskOutputArtifactChannel(abc.ABC):
    def __init__(
            self,
            name: str,
            channel_type: Union[str, Dict],
            task_name: Optional[str] = None,
            parties: Optional[List[PartySpec]] = None
    ):
        self.name = name
        self.channel_type = channel_type
        self.task_name = task_name or None
        self.source = ArtifactSourceType.TASK_OUTPUT_ARTIFACT
        self.parties = parties

    def get_spec(self, **kwargs):
        parties = kwargs.get("parties", None) if kwargs else None
        return RuntimeTaskOutputChannelSpec(
            producer_task=self.task_name,
            output_artifact_key=self.name,
            parties=parties
        )

    def __str__(self):
        return "{" + f"channel:task={self.task_name};" \
                     f"name={self.name};" \
                     f"type={self.channel_type};" \
                     f"source={self.source};"\
                     f"parties={self.parties}"+ "}"

    def __repr__(self):
        return str(self)


class DataWarehouseChannel(abc.ABC):
    def __init__(
            self,
            name: str = None,
            namespace: str = None,
            dataset_id: str = None,
            parties: Optional[Union[dict, List[PartySpec]]] = None,
    ):
        self.name = name
        self.namespace = namespace
        self.dataset_id = dataset_id
        self.parties = parties
        self.source = ArtifactSourceType.DATA_WAREHOUSE

    def get_spec(self, **kwargs):
        parties = kwargs.get("parties", None) if kwargs else None
        return DataWarehouseChannelSpec(
            name=self.name,
            namespace=self.namespace,
            dataset_id=self.dataset_id,
            parties=parties
        )

    def __str__(self):
        return "{" + f"channel:name={self.name};" \
                     f"namespace={self.namespace};" \
                     f"dataset_id={self.dataset_id};" \
                     f"parties={self.parties};" \
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
        parties: dict
    ):
        self.model_id = model_id
        self.model_version = model_version
        self.producer_task = producer_task
        self.output_artifact_key = output_artifact_key
        self.parties = parties
        self.source = ArtifactSourceType.MODEL_WAREHOUSE

    def get_spec(self, **kwargs):
        return ModelWarehouseChannelSpec(
            model_id=self.model_id,
            model_version=self.model_version,
            producer_task=self.producer_task,
            output_artifact_key=self.output_artifact_key,
            parties=self.parties
        )

    def __str__(self):
        return "{" + f"channel:model_id={self.model_id};" \
                     f"model_version={self.model_version};" \
                     f"producer_task={self.producer_task};" \
                     f"output_artifact_key={self.output_artifact_key};" \
                     f"parites={self.parties};" \
                     f"source={self.source};" + "}"

    def __repr__(self):
        return str(self)


ArtifactType = TypeVar("ArtifactType",
                       TaskOutputArtifactChannel,
                       DataWarehouseChannel,
                       ModelWarehouseChannel)
