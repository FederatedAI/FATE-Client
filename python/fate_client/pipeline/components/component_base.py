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
import uuid

from types import SimpleNamespace
from typing import List

from ..conf.types import SupportRole, PlaceHolder, ArtifactSourceType, InputArtifactType, OutputArtifactType
from ..conf.job_configuration import TaskConf
from ..entity.component_structures import load_component_spec
from ..interface import TaskOutputArtifactChannel, DataWarehouseChannel, ModelWarehouseChannel
from ..entity.dag_structures import OutputArtifactSpec, PartySpec
from ..entity.runtime_entity import Parties


class Component(object):
    __instance = {}

    yaml_define_path = None

    def __init__(self, *args, **kwargs):
        self._name = None
        self.runtime_parties = Parties()
        self.__party_instance = {}
        self._module = None
        self._role = None
        self._index = None
        self._callable = True
        self._outputs = None
        self._task_parameters = dict()
        self._task_conf = TaskConf()
        self._stage = None

        if self.yaml_define_path is None:
            raise ValueError("Component should have yaml define file, set yaml_define_path first please!")

        self._component_spec = load_component_spec(self.yaml_define_path)
        self._provider = None
        self._version = None
        self._init_task_setting()

    def __new__(cls, *args, **kwargs):
        if cls.__name__.lower() not in cls.__instance:
            cls.__instance[cls.__name__.lower()] = 0

        new_cls = object.__new__(cls)
        new_cls.set_name(cls.__instance[cls.__name__.lower()])
        cls.__instance[cls.__name__.lower()] += 1

        return new_cls

    def set_name(self, idx):
        self._name = self.__class__.__name__.lower() + "_" + str(idx)

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

    @property
    def stage(self):
        return self._stage

    @stage.setter
    def stage(self, stage):
        self._stage = stage

    def get_party_instance(self, role="guest") -> 'Component':
        if role not in self.support_roles:
            raise ValueError("Role should be one of guest/host/arbiter")

        if role not in self.__party_instance:
            self.__party_instance[role] = dict()

        index = str(uuid.uuid1())

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
    def task_name(self):
        return self._name

    @property
    def component_ref(self):
        return self._component_spec.name

    @property
    def conf(self):
        return self._task_conf

    @property
    def support_roles(self):
        self._convert_party_dict_to_party_inst()
        if not len(self.runtime_parties):
            return self._component_spec.roles
        else:
            return list(set(self._component_spec.roles) & set(self.runtime_parties.get_runtime_roles()))

    @property
    def support_parties(self) -> Parties:
        self._convert_party_dict_to_party_inst()
        return self.runtime_parties

    def task_parameters(self, **kwargs):
        for attr, val in kwargs.items():
            self._task_parameters[attr] = val

    def get_task_parameters(self):
        return self._task_parameters

    def get_role_parameters(self, role, index):
        task_parameters = dict()
        if role not in self.__party_instance:
            return task_parameters

        index = str(index)

        role_inst_dict = self.__party_instance[role]

        for _, inst in role_inst_dict.items():
            for party_index, party_inst in inst.party_instance.items():
                party_index = party_index.split("|")
                if index not in party_index:
                    continue

                task_parameters.update(party_inst.get_task_parameters())

        return task_parameters

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
    def provider(self):
        return self._provider

    @property
    def version(self):
        return self._version

    def _get_output_by_parties(self, parties: Parties):
        _outputs = dict()
        for output_artifact_type in OutputArtifactType.types():
            artifacts = getattr(self._component_spec.output_artifacts, output_artifact_type)
            if not artifacts:
                continue

            for artifact_name, artifact in artifacts.items():
                channel = TaskOutputArtifactChannel(
                    name=artifact_name,
                    channel_type=artifact.types[0],
                    task_name=self._name,
                    parties=parties.get_parties_spec()
                )

                _outputs[artifact_name] = channel

        return _outputs

    @property
    def outputs(self):
        if self._component_spec.output_artifacts is None:
            raise ValueError("Output Definitions is None")

        if self._outputs:
            return self._outputs

        self._outputs = dict()

        self._convert_party_dict_to_party_inst()
        self._outputs = self._get_output_by_parties(self.runtime_parties)

        return self._outputs

    def party_outputs(self, parties: dict):
        if not parties:
            raise ValueError("To get party_outputs, pleas pass parties setting")

        party_inst = Parties()
        for role, party_id in parties.items():
            party_inst.set_party(role=role, party_id=party_id)

        return self._get_output_by_parties(parties=party_inst)

    def get_output_artifacts(self):
        outputs = dict()

        for output_artifact_type in OutputArtifactType.types():
            artifacts = getattr(self._component_spec.output_artifacts, output_artifact_type)
            if not artifacts:
                continue

            if output_artifact_type not in outputs:
                outputs[output_artifact_type] = dict()

            for artifact_name, artifact in artifacts.items():
                outputs[output_artifact_type][artifact_name] = OutputArtifactSpec(
                    output_artifact_key_alias=artifact_name,
                    output_artifact_type_alias=output_artifact_type
                )

        return outputs

    def _process_init_inputs(self, inputs):
        self._init_inputs = {}
        for key, value in inputs.items():
            if key == "self" or (key.startswith("_") and key != "_name"):
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
                        raise ValueError(f"Component {self._name}'s {artifact_key} "
                                         f"should be ArtifactChannel, {channel} find")

                    if channel.source == ArtifactSourceType.TASK_OUTPUT_ARTIFACT:
                        dependencies.add(channel.task_name)

        return list(dependencies)

    def get_runtime_input_artifacts(self, dag_runtime_parties: Parties):
        input_artifacts_dict = dict()
        for input_artifact_type in InputArtifactType.types():
            input_artifacts_dict[input_artifact_type] = getattr(self._component_spec.input_artifacts,
                                                                input_artifact_type)

        runtime_input_channels = dict()
        input_artifacts = dict()

        def _channel_parties_to_party_inst(channel_parties):
            channel_party_inst = Parties()
            if isinstance(channel_parties, dict):
                for role, party_id in channel_parties.items():
                    channel_party_inst.set_party(role=role, party_id=party_id)
            else:
                for party_spec in channel_parties:
                    channel_party_inst.set_party(role=party_spec.role, party_id=party_spec.party_id)

            return channel_party_inst

        self._convert_party_dict_to_party_inst()
        for input_artifact_type, artifacts in input_artifacts_dict.items():
            if not artifacts:
                continue

            input_artifacts[input_artifact_type] = dict()
            runtime_input_channels[input_artifact_type] = dict()
            for artifact_key, artifact_spec in artifacts.items():
                if not hasattr(self, artifact_key) or isinstance(getattr(self, artifact_key), PlaceHolder):
                    continue

                channels = getattr(self, artifact_key)

                cpn_runtime_parties = self.runtime_parties if len(self.runtime_parties) else dag_runtime_parties
                cpn_runtime_parties = cpn_runtime_parties.intersect(dag_runtime_parties)
                cpn_runtime_parties = cpn_runtime_parties.get_party_inst_by_role(artifact_spec.roles)

                if not isinstance(channels, list) and artifact_spec.is_multi:
                    channels = [channels]

                if isinstance(channels, list):
                    artifact_list = []
                    for channel in channels:
                        if not channel.parties:
                            artifact = channel.get_spec(parties=cpn_runtime_parties.get_parties_spec())
                        else:
                            artifact = channel.get_spec(
                                parties=cpn_runtime_parties.intersect(
                                    _channel_parties_to_party_inst(channel.parties)
                                ).get_parties_spec()
                            )

                        artifact_list.append(artifact)

                    runtime_input_channels[input_artifact_type][artifact_key] = {channels[0].source: artifact_list}
                    input_artifacts[input_artifact_type][artifact_key] = artifact_spec
                else:
                    if not channels.parties:
                        artifact = channels.get_spec(parties=cpn_runtime_parties.get_parties_spec())
                    else:
                        artifact = channels.get_spec(
                            parties=cpn_runtime_parties.intersect(
                                _channel_parties_to_party_inst(channels.parties)
                            ).get_parties_spec()
                        )

                    runtime_input_channels[input_artifact_type][artifact_key] = {channels.source: artifact}
                    input_artifacts[input_artifact_type][artifact_key] = artifact_spec

        return runtime_input_channels, input_artifacts

    def _init_task_setting(self):
        parameters = self._component_spec.parameters
        for param in parameters:
            if isinstance(self._init_inputs.get(param, PlaceHolder()), PlaceHolder):
                continue
            self._task_parameters[param] = self._init_inputs[param]

        self._provider = self._component_spec.provider
        self._version = self._component_spec.version

    def _convert_party_dict_to_party_inst(self):
        if not self.runtime_parties:
            self.runtime_parties = Parties()
        elif isinstance(self.runtime_parties, dict):
            runtime_parties = Parties()
            for role, party_id in self.runtime_parties.items():
                if role in self.component_spec.roles:
                    runtime_parties.set_party(role=role, party_id=party_id)
            self.runtime_parties = runtime_parties
