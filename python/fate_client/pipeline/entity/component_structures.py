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
from typing import Optional, Dict, List, Union, Any
from pathlib import Path
from pydantic import BaseModel
from ..utils.file_utils import load_yaml_file

TypeSpecType = Union[str, Dict, List]


class ParameterSpec(BaseModel):
    type: str
    default: Any
    optional: bool
    description: str = ""
    type_meta: dict = {}


class ArtifactSpec(BaseModel):
    types: List[str]
    optional: bool
    stages: Optional[List[str]]
    roles: Optional[List[str]]
    description: str = ""
    is_multi: bool


class InputArtifactsSpec(BaseModel):
    data: Dict[str, ArtifactSpec]
    model: Dict[str, ArtifactSpec]


class OutputArtifactsSpec(BaseModel):
    data: Dict[str, ArtifactSpec]
    model: Dict[str, ArtifactSpec]
    metric: Dict[str, ArtifactSpec]


class ComponentSpec(BaseModel):
    name: str
    description: str
    provider: str
    version: str
    labels: List[str] = ["trainable"]
    roles: List[str]
    parameters: Dict[str, ParameterSpec]
    input_artifacts: InputArtifactsSpec
    output_artifacts: OutputArtifactsSpec


class RuntimeOutputChannelSpec(BaseModel):
    producer_task: str
    output_artifact_key: str


class RuntimeInputDefinition(BaseModel):
    parameters: Optional[Dict[str, Any]]
    artifacts: Optional[Dict[str, Dict[str, RuntimeOutputChannelSpec]]]


def load_component_spec(yaml_define_path: str):
    yaml_define_path = Path(__file__).parent.parent.joinpath(yaml_define_path).resolve()
    component_spec_dict = load_yaml_file(str(yaml_define_path))["component"]
    parameters = dict()
    if "parameters" in component_spec_dict:
        for key, value in component_spec_dict["parameters"].items():
            parameters[key] = ParameterSpec(**value)

    input_artifacts = dict(data=dict(),
                           model=dict())
    if "input_artifacts" in component_spec_dict:
        input_artifacts_spec = component_spec_dict["input_artifacts"]

        input_keys = ["data", "model"]
        for input_key in input_keys:
            if input_key not in input_artifacts_spec:
                continue

            for key, value in input_artifacts_spec[input_key].items():
                input_artifacts[input_key][key] = value

    output_artifacts = dict(data=dict(),
                            model=dict(),
                            metric=dict())

    if "output_artifacts" in component_spec_dict:
        output_artifacts_spec = component_spec_dict["output_artifacts"]

        output_keys = ["data", "model", "metric"]
        for output_key in output_keys:
            if output_key not in output_artifacts_spec:
                continue
            for key, value in output_artifacts_spec[output_key].items():
                output_artifacts[output_key][key] = ArtifactSpec(**value)

    input_artifacts = InputArtifactsSpec(**input_artifacts)

    output_artifacts = OutputArtifactsSpec(**output_artifacts)

    return ComponentSpec(
        name=component_spec_dict["name"],
        description=component_spec_dict["description"],
        provider=component_spec_dict["provider"],
        version=component_spec_dict["version"],
        labels=component_spec_dict["labels"],
        roles=component_spec_dict["roles"],
        parameters=parameters,
        input_artifacts=input_artifacts,
        output_artifacts=output_artifacts
    )
