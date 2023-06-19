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
import copy
from ..conf.types import SupportRole, PlaceHolder, ArtifactSourceType, InputArtifactType, OutputArtifactType
from ..conf.job_configuration import TaskConf
from ..utils.standalone.id_gen import get_uuid
from ..entity.component_structures import load_component_spec
from ..interface import TaskOutputArtifactChannel, DataWarehouseChannel, ModelWarehouseChannel
from ..entity.dag_structures import RuntimeTaskOutputChannelSpec, DataWarehouseChannelSpec, ModelWarehouseChannelSpec


class Component(object):
    __instance = {}

    yaml_define_path = None

    def __init__(self, *args, **kwargs):
        self.__name = None
        self.runtime_roles = None
        self.__party_instance = {}
        self._module = None
        self._role = None
        self._index = None
        self._callable = True
        self._outputs = None
        self._component_setting = dict()
        self._task_conf = TaskConf()

        if self.yaml_define_path is None:
            raise ValueError("Component should have yaml define file, set yaml_define_path first please!")

        self._component_spec = load_component_spec(self.yaml_define_path)
        self._init_component_setting()

    def __new__(cls, *args, **kwargs):
        if cls.__name__.lower() not in cls.__instance:
            cls.__instance[cls.__name__.lower()] = 0

        new_cls = object.__new__(cls)
        new_cls.set_name(cls.__instance[cls.__name__.lower()])
        cls.__instance[cls.__name__.lower()] += 1

        return new_cls

    def set_name(self, idx):
        self.__name = self.__class__.__name__.lower() + "_" + str(idx)

    def _set_role(self, role):
        self._role = role

    def _set_index(self, idx):
        self._index = idx

    def _set_callable(self, status):
        self._callable = status

    def callable(self):
        return self._callable

    def __getitem__(self, index) -> "Component":
        if not isinstance(index, (int, list, slice)):
            raise ValueError("Index should be int or list of integer")

        if isinstance(index, slice):
            if index.start is None or index.stop is None:
                raise ValueError(f"Slice {index} is not support, start and stop should be given")
            start = index.start
            stop = index.stop
            step = index.step if index.step else 1 if start < stop else -1
            index = [idx for idx in range(start, stop, step)]
            if len(index) == 1:
                index = index[0]

        if isinstance(index, list):
            index.sort()
        index_key = str(index) if isinstance(index, int) else "|".join(map(str, index))

        # del self.__party_instance[self._role]["party"][self._index]
        self._set_index(index_key)
        self._set_callable(True)

        self.__party_instance[self._index] = copy.deepcopy(self)
        return self.__party_instance[self._index]

    @property
    def guest(self) -> "Component":
        inst = self.get_party_instance(role=SupportRole.GUEST)[0]
        return inst

    @property
    def hosts(self) -> "Component":
        inst = self.get_party_instance(role=SupportRole.HOST)
        return inst

    @property
    def arbiter(self) -> "Component":
        inst = self.get_party_instance(role=SupportRole.ARBITER)[0]
        return inst

    def get_party_instance(self, role="guest") -> 'Component':
        if role not in self.support_roles:
            raise ValueError("Role should be one of guest/host/arbiter")

        if role not in self.__party_instance:
            self.__party_instance[role] = dict()

        index = get_uuid()

        inst = copy.deepcopy(self)
        inst.party_instance = {}
        self._decrease_instance_count()

        inst._set_role(role)
        inst._set_index(index)
        inst._set_callable(False)

        self.__party_instance[role][index] = inst
        return inst

    @classmethod
    def _decrease_instance_count(cls):
        cls.__instance[cls.__name__.lower()] -= 1

    @property
    def party_instance(self):
        return self.__party_instance

    @party_instance.setter
    def party_instance(self, party_instance):
        self.__party_instance = party_instance

    @property
    def get_name(self):
        return self.__name

    @property
    def component_ref(self):
        return self._component_spec.name

    @property
    def conf(self):
        return self._task_conf

    @property
    def support_roles(self):
        if not self.runtime_roles:
            return self._component_spec.roles
        else:
            if not isinstance(self.runtime_roles, list):
                self.runtime_roles = [self.runtime_roles]
            return list(set(self._component_spec.roles) & set(self.runtime_roles))

    def component_setting(self, **kwargs):
        for attr, val in kwargs.items():
            self._component_setting[attr] = val

    def get_component_setting(self):
        return self._component_setting

    def get_role_setting(self, role, index):
        component_setting = dict()
        if role not in self.__party_instance:
            return component_setting

        index = str(index)

        role_inst_dict = self.__party_instance[role]

        for _, inst in role_inst_dict.items():
            for party_index, party_inst in inst.party_instance.items():
                party_index = party_index.split("|")
                if index not in party_index:
                    continue

                component_setting.update(party_inst.get_component_setting())

        if not component_setting:
            return component_setting

        parameters = {}
        inputs = {}
        for attr, value in component_setting.items():
            if attr in self._component_spec.parameters:
                parameters[attr] = value
            else:
                """
                artifact
                """
                if not isinstance(value, (DataWarehouseChannel, ModelWarehouseChannel)) or \
                        (isinstance(value, list) and
                         not isinstance(value[0], (DataWarehouseChannelSpec, ModelWarehouseChannelSpec))):
                    raise ValueError(f"attr={attr} should be data_warehouse or model_warehouse artifact")

                if not isinstance(value, list):
                    type_key = InputArtifactType.DATA if isinstance(value, DataWarehouseChannel) \
                        else InputArtifactType.MODEL
                else:
                    type_key = InputArtifactType.DATA if isinstance(value[0], DataWarehouseChannel) \
                        else InputArtifactType.MODEL

                if type_key not in inputs:
                    inputs[type_key] = dict()

                artifact_spec = getattr(self._component_spec.input_artifacts, type_key).get(attr, None)
                if not artifact_spec:
                    raise ValueError(f"attr={attr} does not exist in component spec")

                if isinstance(value, list):
                    artifact_list = [v.get_spec(roles=[role]) for v in value]
                    inputs[type_key][attr] = {value[0].source: artifact_list}
                else:
                    inputs[type_key][attr] = {value.source: value.get_spec(roles=[role])}

        component_setting = dict()
        if parameters:
            component_setting["parameters"] = parameters
        if inputs:
            component_setting["inputs"] = inputs

        return component_setting

    def get_role_conf(self, role, index):
        conf = dict()
        if role not in self.__party_instance:
            return conf

        index = str(index)
        role_inst_dict = self.__party_instance[role]

        for _, inst in role_inst_dict.items():
            for party_index, party_inst in inst.party_instance.items():
                party_index = party_index.split("|")
                if index not in party_index:
                    continue

                conf.update(party_inst.conf.dict())

        return conf

    def validate_runtime_env(self, roles):
        runtime_roles = roles.get_runtime_roles()
        for role, role_inst in self.__party_instance.items():
            if role not in runtime_roles:
                raise ValueError(f"role {role} does not set in pipeline")
            runtime_role_parties = roles.get_party_list_by_role(role)

            mx_idx = 0
            for _, inst in role_inst.items():
                for party_key in inst.party_instance:
                    parties = map(int, party_key.split("|", -1))
                    mx_idx = max(mx_idx, max(parties))

            if mx_idx >= len(runtime_role_parties):
                raise ValueError(f"role {role}, index {mx_idx} out of bound")

    @property
    def component_spec(self):
        return self._component_spec

    @property
    def outputs(self):
        if self._component_spec.output_artifacts is None:
            raise ValueError("Output Definitions is None")

        if self._outputs:
            return self._outputs

        for output_artifact_type in OutputArtifactType.types():
            artifacts = getattr(self._component_spec.output_artifacts, output_artifact_type)
            if not artifacts:
                continue

            self._outputs = dict()
            for artifact_name, artifact in artifacts.items():
                channel = TaskOutputArtifactChannel(
                    name=artifact_name,
                    channel_type=artifact.type,
                    task_name=self.name
                )

                self._outputs[artifact_name] = channel

        return self._outputs

    def _process_init_inputs(self, inputs):
        self._init_inputs = {}
        for key, value in inputs.items():
            if key == "self" or key.startswith("_"):
                continue

            self._init_inputs[key] = value

    def get_dependent_tasks(self):
        if not hasattr(self._component_spec, "input_artifacts"):
            return []
        input_artifacts = self._component_spec.input_artifacts
        dependencies = set()

        for artifact_type in InputArtifactType.types():
            for artifact_key in getattr(input_artifacts, artifact_type):
                if not hasattr(self, artifact_key) or isinstance(getattr(self, artifact_key), PlaceHolder):
                    continue

                channels = getattr(self, artifact_key)
                if not channels:
                    continue

                if not isinstance(channels, list):
                    channels = [channels]

                for channel in channels:
                    if not isinstance(channel, (TaskOutputArtifactChannel, DataWarehouseChannel, ModelWarehouseChannel)):
                        raise ValueError(f"Component {self.__name}'s {artifact_key} "
                                         f"should be ArtifactChannel, {channel} find")

                    if channel.source == ArtifactSourceType.TASK_OUTPUT_ARTIFACT:
                        dependencies.add(channel.task_name)

        return list(dependencies)

    def get_runtime_input_artifacts(self, runtime_roles):
        input_artifacts_dict = dict()
        for input_artifact_type in InputArtifactType.types():
            input_artifacts_dict[input_artifact_type] = getattr(self._component_spec.input_artifacts,
                                                                input_artifact_type)

        runtime_input_channels = dict()
        input_artifacts = dict()

        for input_artifact_type, artifacts in input_artifacts_dict.items():
            if not artifacts:
                continue

            input_artifacts[input_artifact_type] = dict()
            runtime_input_channels[input_artifact_type] = dict()
            for artifact_key, artifact_spec in artifacts.items():
                if not hasattr(self, artifact_key) or isinstance(getattr(self, artifact_key), PlaceHolder):
                    continue

                channels = getattr(self, artifact_key)

                roles = list(set(runtime_roles) & set(artifact_spec.roles)) \
                    if set(runtime_roles) != set(artifact_spec.roles) else None

                if isinstance(channels, list) and not artifact_spec.is_multi:
                    raise ValueError(f"Artifact={artifact_key}'s input is list, it should be a single input")
                if not isinstance(channels, list) and artifact_spec.is_multi:
                    channels = [channels]

                if isinstance(channels, list):
                    artifact_list = []
                    for channel in channels:
                        artifact = channel.get_spec(roles=roles)
                        artifact_list.append(artifact)

                    runtime_input_channels[input_artifact_type][artifact_key] = {channels[0].source: artifact_list}
                    input_artifacts[input_artifact_type][artifact_key] = artifact_spec
                else:
                    artifact = channels.get_spec(roles=roles)
                    runtime_input_channels[input_artifact_type][artifact_key] = {channels.source: artifact}
                    input_artifacts[input_artifact_type][artifact_key] = artifact_spec

        return runtime_input_channels, input_artifacts

    def _init_component_setting(self):
        parameters = self._component_spec.parameters
        for param in parameters:
            if isinstance(self._init_inputs.get(param, PlaceHolder()), PlaceHolder):
                continue
            self._component_setting[param] = self._init_inputs[param]
