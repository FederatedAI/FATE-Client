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
from typing import Dict
from .component_spec import BFIAComponentSpec
from fate_client.pipeline.entity.component_structures import (
    ArtifactSpec,
    ComponentSpec,
    ParameterSpec,
    InputArtifactsSpec,
    OutputArtifactsSpec
)
from .utils.types import get_source_type


class ComponentTranslator(object):
    @classmethod
    def translate_to_component_spec(cls, bfia_component_spec: BFIAComponentSpec) -> ComponentSpec:
        return dict(
            component=ComponentSpec(
                name=bfia_component_spec.componentName,
                description=bfia_component_spec.description,
                provider=bfia_component_spec.provider,
                version=bfia_component_spec.version,
                labels=[''],
                roles=bfia_component_spec.roleList,
                parameters=cls.translate_to_parameters_spec(bfia_component_spec),
                input_artifacts=InputArtifactsSpec(**cls.translate_to_io_artifacts(bfia_component_spec, "inputData")),
                output_artifacts=OutputArtifactsSpec(**cls.translate_to_io_artifacts(bfia_component_spec, "outputData"))
            ).dict(exclude_defaults=True)
        )

    @classmethod
    def translate_to_io_artifacts(cls, bfia_component_spec: BFIAComponentSpec, data_key):
        if not bfia_component_spec.inputData:
            return None

        if data_key == "inputData":
            artifact_dict = dict(data={},
                                 model={})
        else:
            artifact_dict = dict(
                data={},
                model={},
                metric={}
            )
        for data in getattr(bfia_component_spec, data_key):
            artifact_type = get_source_type(data.category)

            if artifact_type not in artifact_dict:
                artifact_dict[artifact_type] = dict()

            artifact_name = data.name
            artifact_dict[artifact_type][artifact_name] = ArtifactSpec(
                types=data.dataFormat,
                optional=True,
                stages=["train", "predict"] if "train" in artifact_name or "test" in artifact_name else ["default"],
                roles=bfia_component_spec.roleList,
                description=getattr(bfia_component_spec, "description", ''),
                is_multi=False
            )

        return artifact_dict

    @classmethod
    def translate_to_parameters_spec(cls, bfia_component_spec: BFIAComponentSpec) -> Dict[str, ParameterSpec]:
        if not bfia_component_spec.inputParam:
            return dict()

        params_spec = dict()
        for input_param in bfia_component_spec.inputParam:
            param_name = input_param["name"]
            params_spec[param_name] = ParameterSpec(
                type=input_param["type"],
                default=input_param.get("defaultValue", None),
                description=input_param.get("description", ''),
                optional=input_param.get("optional", True)
           )

        return params_spec
