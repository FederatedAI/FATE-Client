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
import networkx as nx

from pydantic import BaseModel
from typing import Dict, List, Union

from ..conf.types import (
    Stage,
    InputDataKeyType,
    ArtifactSourceType,
    InputArtifactType,
    OutputArtifactType,
)

from ..entity.dag_structures import (
    DAGSchema,
    DAGSpec,
    RuntimeTaskOutputChannelSpec,
    ModelWarehouseChannelSpec,
    DataWarehouseChannelSpec,
    PartySpec
)
from ..entity.component_structures import ArtifactSpec, ComponentSpec, InputArtifactsSpec, OutputArtifactsSpec


class DagParser(object):
    def __init__(self):
        self._dag = dict()
        self._global_dag = nx.DiGraph()
        self._links = dict()
        self._tasks = dict()
        self._task_runtime_parties = dict()
        self._conf = dict()

    def parse_dag(self, dag_schema: DAGSchema, component_specs: Dict[str, ComponentSpec] = None):
        dag_spec = dag_schema.dag
        dag_stage = dag_spec.stage
        tasks = dag_spec.tasks
        if dag_spec.conf:
            self._conf = dag_spec.conf.dict(exclude_defaults=True)
        job_conf = self._conf.get("task", {})

        for party in dag_spec.parties:
            if party.role not in self._dag:
                self._dag[party.role] = dict()
            for party_id in party.party_id:
                self._dag[party.role][party_id] = nx.DiGraph()

        for name, task_spec in tasks.items():
            parties = task_spec.parties if task_spec.parties else dag_spec.parties
            task_stage = dag_stage
            component_ref = task_spec.component_ref
            if task_spec.stage:
                task_stage = task_spec.stage

            self._global_dag.add_node(name, component_ref=component_ref)

            self._task_runtime_parties[name] = parties

            for party_spec in parties:
                if party_spec.role not in self._tasks:
                    self._tasks[party_spec.role] = dict()
                for party_id in party_spec.party_id:
                    self._dag[party_spec.role][party_id].add_node(name)
                    if party_id not in self._tasks[party_spec.role]:
                        self._tasks[party_spec.role][party_id] = dict()
                    self._tasks[party_spec.role][party_id].update({
                        name: TaskNodeInfo()
                    })
                    self._tasks[party_spec.role][party_id][name].stage = task_stage
                    self._tasks[party_spec.role][party_id][name].component_ref = component_ref
                    if component_specs:
                        self._tasks[party_spec.role][party_id][name].component_spec = component_specs[name]

        for name, task_spec in tasks.items():
            if not task_spec.conf:
                task_conf = copy.deepcopy(job_conf)
            else:
                task_conf = copy.deepcopy(job_conf)
                task_conf.update(task_spec.conf)

            self._init_task_runtime_parameters_and_conf(name, dag_schema, task_conf)

            self._init_upstream_inputs(name, dag_schema.dag)
            self._init_outputs(name, dag_schema.dag)

    def _init_upstream_inputs(self, name, dag: DAGSpec):
        task_spec = dag.tasks[name]
        upstream_inputs = dict()

        parties = task_spec.parties if task_spec.parties else dag.parties
        for party in parties:
            if party.role not in upstream_inputs:
                upstream_inputs[party.role] = dict()
            for party_id in party.party_id:
                self._tasks[party.role][party_id][name].upstream_inputs = self._get_upstream_inputs(
                    name, task_spec, party.role, party_id
                )

    def _get_upstream_inputs(self, name, task_spec, role, party_id):
        upstream_inputs = dict()
        runtime_parties = task_spec.parties

        if runtime_parties:
            runtime_parties_dict = dict((party.role, party.party_id) for party in runtime_parties)
            if role not in runtime_parties_dict or party_id not in runtime_parties_dict[role]:
                return upstream_inputs

        input_artifacts = task_spec.inputs

        if not input_artifacts:
            return upstream_inputs

        for input_type in InputArtifactType.types():
            artifacts = getattr(input_artifacts, input_type)
            if not artifacts:
                continue

            for input_key, output_specs_dict in artifacts.items():
                for artifact_source, channel_spec_list in output_specs_dict.items():
                    if artifact_source == ArtifactSourceType.MODEL_WAREHOUSE:
                        is_list = True
                        if not isinstance(channel_spec_list, list):
                            is_list = False
                            channel_spec_list = [channel_spec_list]
                        inputs = []
                        for channel in channel_spec_list:
                            model_warehouse_channel = ModelWarehouseChannelSpec(**channel.dict(exclude_defaults=True))
                            if model_warehouse_channel.parties and not self.task_can_run(
                                    role, party_id, runtime_parties=model_warehouse_channel.parties):
                                continue

                            if model_warehouse_channel.model_id is None:
                                model_warehouse_channel.model_id = \
                                    self._conf.get("model_warehouse", {}).get("model_id", None)
                                model_warehouse_channel.model_version = \
                                    self._conf.get("model_warehouse", {}).get("model_version", None)
                            inputs.append(model_warehouse_channel)

                        if not inputs:
                            continue

                        if input_type not in upstream_inputs:
                            upstream_inputs[input_type] = dict()

                        if is_list and len(inputs) == 1:
                            is_list = False
                        upstream_inputs[input_type][input_key] = inputs if is_list else inputs[0]
                    elif artifact_source == ArtifactSourceType.DATA_WAREHOUSE:
                        is_list = True
                        if not isinstance(channel_spec_list, list):
                            is_list = False
                            channel_spec_list = [channel_spec_list]
                        inputs = []
                        for channel in channel_spec_list:
                            if channel.parties and \
                                    not self.task_can_run(role, party_id, runtime_parties=channel.parties):
                                continue
                            inputs.append(DataWarehouseChannelSpec(**channel.dict(exclude_defaults=True)))

                        if not inputs:
                            continue
                        if input_type not in upstream_inputs:
                            upstream_inputs[input_type] = dict()

                        if is_list and len(inputs) == 1:
                            is_list = False
                        upstream_inputs[input_type][input_key] = inputs if is_list else inputs[0]
                    else:
                        if not isinstance(channel_spec_list, list):
                            channel_spec_list = [channel_spec_list]

                        filter_channel_spec_list = []
                        for channel_spec in channel_spec_list:
                            if channel_spec.parties:
                                parties_dict = dict((party.role, party.party_id) for party in channel_spec.parties)
                                if role not in parties_dict or party_id not in parties_dict[role]:
                                    continue
                            else:
                                if channel_spec.producer_task not in self._dag[role][party_id].nodes:
                                    continue
                            filter_channel_spec_list.append(channel_spec)

                        if not filter_channel_spec_list:
                            continue

                        if len(filter_channel_spec_list) > 1:
                            inputs = [RuntimeTaskOutputChannelSpec(**channel.dict(exclude_defaults=True))
                                      for channel in filter_channel_spec_list]
                        else:
                            inputs = RuntimeTaskOutputChannelSpec(**filter_channel_spec_list[0].dict(exclude_defaults=True))

                        if not inputs:
                            continue

                        if input_type not in upstream_inputs:
                            upstream_inputs[input_type] = dict()
                        upstream_inputs[input_type][input_key] = inputs

                        for channel_spec in filter_channel_spec_list:
                            dependent_task = channel_spec.producer_task
                            self._add_edge(dependent_task, name, role, party_id)

        upstream_inputs = self.check_and_add_runtime_party(upstream_inputs, role, party_id, artifact_type="input")

        return upstream_inputs

    def _init_outputs(self, name, dag: DAGSpec):
        task_spec = dag.tasks[name]

        if not task_spec.outputs:
            return

        parties = task_spec.parties if task_spec.parties else dag.parties

        for output_type, outputs_dict in iter(task_spec.outputs):
            if not outputs_dict:
                continue

            for outputs_key, output_artifact in outputs_dict.items():
                output_parties = output_artifact.parties if output_artifact.parties else parties
                for party_spec in output_parties:
                    for party_id in party_spec.party_id:
                        if not self.task_can_run(party_spec.role, party_id, runtime_parties=parties):
                            continue

                        if outputs_key not in self._tasks[party_spec.role][party_id][name].outputs:
                            self._tasks[party_spec.role][party_id][name].outputs[output_type] = dict()

                        self._tasks[party_spec.role][party_id][name].outputs[output_type][outputs_key] = output_artifact

        for party_spec in parties:
            for party_id in party_spec.party_id:
                self._tasks[party_spec.role][party_id][name].outputs = self.check_and_add_runtime_party(
                    self._tasks[party_spec.role][party_id][name].outputs,
                    party_spec.role,
                    party_id,
                    artifact_type="output"
                )

    def _add_edge(self, src, dst, role, party_id, attrs=None):
        if not attrs:
            attrs = {}

        self._dag[role][party_id].add_edge(src, dst, **attrs)
        self._global_dag.add_edge(src, dst, **attrs)

    def _init_task_runtime_parameters_and_conf(self, task_name: str, dag_schema: DAGSchema, global_task_conf):
        dag = dag_schema.dag
        task_spec = dag.tasks[task_name]

        common_parameters = dict()
        if task_spec.parameters:
            common_parameters = task_spec.parameters

        parties = dag.parties if not task_spec.parties else task_spec.parties

        for party in parties:
            for party_id in party.party_id:
                self._tasks[party.role][party_id][task_name].runtime_parameters = copy.deepcopy(common_parameters)
                self._tasks[party.role][party_id][task_name].conf = copy.deepcopy(global_task_conf)

        if dag.party_tasks:
            party_tasks = dag.party_tasks
            for site_name, party_tasks_spec in party_tasks.items():
                if party_tasks_spec.conf:
                    for party in party_tasks_spec.parties:
                        for party_id in party.party_id:
                            self._tasks[party.role][party_id][task_name].conf.update(party_tasks_spec.conf)

                if not party_tasks_spec.tasks or task_name not in party_tasks_spec.tasks:
                    continue

                party_parties = party_tasks_spec.parties
                party_task_spec = party_tasks_spec.tasks[task_name]

                if party_task_spec.conf:
                    for party in party_parties:
                        for party_id in party.party_id:
                            self._tasks[party.role][party_id][task_name].conf.update(party_task_spec.conf)

                parameters = party_task_spec.parameters

                if parameters:
                    for party in party_parties:
                        for party_id in party.party_id:
                            self._tasks[party.role][party_id][task_name].runtime_parameters.update(parameters)

    def get_runtime_roles_on_party(self, task_name, party_id):
        task_runtime_parties = self._task_runtime_parties[task_name]

        runtime_roles = set()
        for party_spec in task_runtime_parties:
            if party_id in party_spec.party_id:
                runtime_roles.add(party_spec.role)

        return list(runtime_roles)

    def get_task_node(self, role, party_id, task_name):
        if role not in self._tasks:
            raise ValueError(f"role={role} does ont exist in dag")
        if party_id not in self._tasks[role]:
            raise ValueError(f"role={role}, party_id={party_id} does not exist in dag")
        if task_name not in self._tasks[role][party_id]:
            raise ValueError(f"role={role}, party_id={party_id} does not has task {task_name}")

        return self._tasks[role][party_id][task_name]

    def get_need_revisit_tasks(self, visited_tasks, failed_tasks, role, party_id):
        """
        visited_tasks: already visited tasks
        failed_tasks: failed tasks

        this function finds tasks need to rerun, a task need to rerun if is upstreams is failed
        """
        invalid_tasks = set(self.party_topological_sort(role, party_id)) - set(visited_tasks)
        invalid_tasks |= set(failed_tasks)

        revisit_tasks = []
        for task_to_check in visited_tasks:
            if task_to_check in invalid_tasks:
                revisit_tasks.append(task_to_check)
                continue

            task_valid = True
            task_stack = {task_to_check}
            stack = [task_to_check]

            while len(stack) > 0 and task_valid:
                task = stack.pop()
                pre_tasks = self.party_predecessors(role, party_id, task)

                for pre_task in pre_tasks:
                    if pre_task in task_stack:
                        continue
                    if pre_task in invalid_tasks:
                        task_valid = False
                        break

                    task_stack.add(pre_task)
                    stack.append(pre_task)

            if not task_valid:
                revisit_tasks.append(task_to_check)

        return revisit_tasks

    def global_topological_sort(self):
        return nx.topological_sort(self._global_dag)

    def get_component_ref(self, task_name):
        return self._global_dag.nodes[task_name]["component_ref"]

    def party_topological_sort(self, role, party_id):
        assert role in self._dag or party_id in self._dag[role], f"role={role}, party_id={party_id} does not exist"
        return nx.topological_sort(self._dag[role][party_id])

    def party_predecessors(self, role, party_id, task):
        return set(self._dag[role][party_id].predecessors(task))

    def party_successors(self, role, party_id, task):
        return self._dag[role][party_id].successors(task)

    def get_edge_attr(self, role, party_id, src, dst):
        return self._dag[role][party_id].edges[src, dst]

    @staticmethod
    def check_and_add_runtime_party(artifacts, role, party_id, artifact_type):
        correct_artifacts = copy.deepcopy(artifacts)
        if artifact_type == "input":
            types = InputArtifactType.types()
        else:
            types = OutputArtifactType.types()

        for t in types:
            if t not in artifacts:
                continue
            for _key, channel_list in artifacts[t].items():
                if isinstance(channel_list, list):
                    for idx, channel in enumerate(channel_list):
                        correct_artifacts[t][_key][idx].parties = [PartySpec(role=role, party_id=[party_id])]
                else:
                    correct_artifacts[t][_key].parties = [PartySpec(role=role, party_id=[party_id])]

        return correct_artifacts

    @property
    def conf(self):
        return self._conf

    @property
    def task_runtime_parties(self):
        return self._task_runtime_parties

    def get_task_runtime_parties(self, task_name):
        return self._task_runtime_parties[task_name]

    @classmethod
    def deploy(cls, task_name_list: list, dag_schema: DAGSchema, component_specs: Dict[str, ComponentSpec]):
        dag_parser = DagParser()
        dag_parser.parse_dag(dag_schema, component_specs)

        data_tracer = dict()
        task_name_set = set(task_name_list)
        for task_name in dag_parser.global_topological_sort():
            parties = dag_parser.get_task_runtime_parties(task_name)
            task_tracer = dict()
            for party_spec in parties:
                if party_spec.role not in task_tracer:
                    task_tracer[party_spec.role] = dict()
                for party_id in party_spec.party_id:
                    task_tracer[party_spec.role][party_id] = cls.trace_back_deploy_task(
                        task_name,
                        task_name_set,
                        dag_schema.dag,
                        component_specs,
                        data_tracer,
                        dag_parser.task_runtime_parties,
                        party_spec.role,
                        party_id
                    )
            data_tracer[task_name] = task_tracer

        dag_spec = cls.deduce_dag(dag_parser, task_name_list, dag_schema.dag,
                                  component_specs, data_tracer, dag_parser.task_runtime_parties)
        dag_spec = cls.erase_redundant_tasks(
            task_name_set,
            dag_spec
        )

        return dag_spec

    @classmethod
    def deduce_dag(cls, dag_parser: 'DagParser', task_name_list: list, dag_spec: DAGSpec,
                   component_specs: Dict[str, ComponentSpec], data_tracer: dict,
                   task_runtime_parties: Dict[str, List[PartySpec]]):
        deduced_dag = copy.deepcopy(dag_spec)
        deduced_dag.stage = Stage.PREDICT

        """
        linkage messages only occur in tasks field
        """
        task_name_set = set(task_name_list)
        topological_task_list = list(dag_parser.global_topological_sort())
        for task_name in topological_task_list:
            if task_name not in task_name_set:
                continue

            task = dag_spec.tasks[task_name]
            """
            job stage should be "train", so task.stage is default/predict/None, if stage is predict, erase it
            """
            if task.stage == Stage.PREDICT:
                deduced_dag.tasks[task_name].stage = None

            """
            default stage should not distinguish fit & transform or fit & transform. 
            """
            component_spec = component_specs[task_name]
            if task.inputs and (data_input_artifacts := task.inputs.data):
                for artifact_name, artifact_channel in data_input_artifacts.items():
                    artifact_definition = component_spec.input_artifacts.data[artifact_name]
                    deduced_dag.tasks[task_name].inputs.data.pop(artifact_name)
                    if isinstance(artifact_channel, DataWarehouseChannelSpec) or artifact_name == InputDataKeyType.VALIDATE_DATA:
                        continue
                    elif artifact_name == InputDataKeyType.TRAIN_DATA:
                        """
                        change train_data to test_data, try to infer a test data key in input definition
                        """
                        test_input_key = cls.infer_test_input_data_key(artifact_name,
                                                                       task.inputs.data.keys(),
                                                                       component_spec.input_artifacts.data)
                    else:
                        """
                        test_data/input_data or other data type, it won't be changed if stage is default or predict,
                        else also infer first
                        """
                        if Stage.DEFAULT in artifact_definition.stages or \
                                Stage.PREDICT in artifact_definition.stages:
                            test_input_key = artifact_name
                        else:
                            test_input_key = cls.infer_test_input_data_key(artifact_name,
                                                                           task.inputs.data.keys(),
                                                                           component_spec.input_artifacts.data)

                    test_input_artifact_definition = component_spec.input_artifacts.data[test_input_key]
                    for _, channel_list in artifact_channel.items():
                        if not isinstance(channel_list, list):
                            channel_list = [channel_list]
                        for channel in channel_list:
                            if isinstance(channel, DataWarehouseChannelSpec):
                                continue
                            assert isinstance(channel, RuntimeTaskOutputChannelSpec)
                            parties = channel.parties if channel.parties else task_runtime_parties[channel.producer_task]

                            for party_spec in parties:
                                for party_id in party_spec.party_id:
                                    test_input_data = cls.infer_test_input_data(
                                        artifact_definition,
                                        test_input_artifact_definition,
                                        channel,
                                        dag_spec,
                                        component_specs,
                                        data_tracer,
                                        task_runtime_parties[task_name],
                                        party_spec.role,
                                        party_id
                                    )
                                    if test_input_data:
                                        if test_input_key not in deduced_dag.tasks[task_name].inputs.data:
                                            deduced_dag.tasks[task_name].inputs.data[test_input_key] = dict()
                                        if _ not in deduced_dag.tasks[task_name].inputs.data[test_input_key]:
                                            deduced_dag.tasks[task_name].inputs.data[test_input_key][_] = []
                                        deduced_dag.tasks[task_name].inputs.data[test_input_key][_].extend(test_input_data)

                        if channels := deduced_dag.tasks[task_name].inputs.data.get(test_input_key, {}).get(_):
                            deduced_dag.tasks[task_name].inputs.data[test_input_key][_] = \
                                cls.merge_artifact_channel_by_party(
                                    channels,
                                )

            if task.inputs and (model_input_artifacts := task.inputs.model):
                for artifact_name in model_input_artifacts:
                    deduced_dag.tasks[task_name].inputs.model.pop(artifact_name)

            model_input_artifact_key, model_output_artifact_key = cls.infer_model_artifact(
                component_spec.input_artifacts, component_spec.output_artifacts)
            if model_input_artifact_key and model_output_artifact_key:
                parties = task_runtime_parties[task_name]
                parties = list(filter(
                    lambda party: \
                        party.role in component_specs[task_name].output_artifacts.model[model_output_artifact_key].roles,
                    parties)
                )

                if parties:
                    deduced_dag.tasks[task_name].inputs.model = {
                        model_input_artifact_key: {
                            ArtifactSourceType.MODEL_WAREHOUSE: ModelWarehouseChannelSpec(
                                producer_task=task_name,
                                output_artifact_key=model_output_artifact_key,
                                parties=parties
                            )
                        }
                    }

            if deduced_dag.tasks[task_name].inputs:
                deduced_dag.tasks[task_name].dependent_tasks = cls.infer_dependent_tasks(
                    deduced_dag.tasks[task_name].inputs
                )

        return deduced_dag

    @classmethod
    def erase_redundant_tasks(cls, task_name_set: set, dag_spec: DAGSpec):
        ret_dag = copy.deepcopy(dag_spec)
        for task, task_spec in dag_spec.tasks.items():
            if task not in task_name_set:
                ret_dag.tasks.pop(task)

        if dag_spec.party_tasks:
            for site_name, party_tasks_spec in dag_spec.party_tasks.items():
                if not party_tasks_spec.tasks:
                    continue

                for task_name, task_spec in party_tasks_spec.tasks.items():
                    if task_name not in task_name_set:
                        ret_dag.party_tasks[site_name].tasks.pop(task_name)

        return ret_dag

    @classmethod
    def infer_dependent_tasks(cls, input_artifacts):
        if not input_artifacts:
            return []

        dependent_task_list = list()
        for input_type in InputArtifactType.types():
            artifacts = getattr(input_artifacts, input_type)
            if not artifacts:
                continue
            for artifact_name, artifact_channel in artifacts.items():
                for artifact_source_type, channels in artifact_channel.items():
                    if artifact_source_type in [ArtifactSourceType.MODEL_WAREHOUSE, ArtifactSourceType.DATA_WAREHOUSE]:
                        continue

                    if not isinstance(channels, list):
                        channels = [channels]
                    for channel in channels:
                        dependent_task_list.append(channel.producer_task)

        return dependent_task_list

    @classmethod
    def infer_test_input_data_key(cls, replace_key=None, train_input_keys=None, artifact_definitions=None):
        """
        we assume that training data and test_data should not be configure in same time
        """
        candidate_predict_set = set()
        candidate_default_set = set()
        candidate_training_set = set()
        for input_key, input_spec in artifact_definitions.items():
            if Stage.DEFAULT in input_spec.stages or Stage.PREDICT in input_spec.stages:
                if train_input_keys and input_key in train_input_keys:
                    candidate_training_set.add(input_key)
                elif Stage.DEFAULT in input_spec.stages:
                    candidate_default_set.add(input_key)
                else:
                    candidate_predict_set.add(input_key)

        if candidate_predict_set:
            if len(candidate_predict_set) > 1:
                print("Warning: multiple test input artifact data key exists, choose one randomly")
            return list(candidate_predict_set)[0]

        if candidate_default_set:
            if len(candidate_default_set) > 1:
                print("Warning: multiple test input artifact data key exists, choose one randomly")
            return list(candidate_predict_set)[0]

        if replace_key in candidate_training_set:
            return replace_key

        if not candidate_training_set:
            raise ValueError("Can not infer test input data key")

        return list(candidate_training_set)[0]

    @classmethod
    def infer_model_artifact(cls, input_artifacts: InputArtifactsSpec,
                             output_artifacts: OutputArtifactsSpec):
        model_input_artifact_key, model_output_artifact_key = None, None
        if output_artifacts and output_artifacts.model:
            model_output_artifact_key_candidate = None
            for artifact_name, artifact_spec in output_artifacts.model.items():
                if Stage.TRAIN in artifact_spec.stages:
                    model_output_artifact_key = artifact_name
                elif Stage.DEFAULT in artifact_spec.stages:
                    model_output_artifact_key_candidate = artifact_name

            if not model_output_artifact_key:
                model_output_artifact_key = model_output_artifact_key_candidate

        if input_artifacts and input_artifacts.model:
            for artifact_name, artifact_spec in input_artifacts.model.items():
                if Stage.PREDICT in artifact_spec.stages or Stage.DEFAULT in artifact_spec.stages:
                    model_input_artifact_key = artifact_name

        return model_input_artifact_key, model_output_artifact_key

    @classmethod
    def infer_test_output_data_key(cls, output_artifacts: Dict[str, ArtifactSpec]):
        candidate_artifact_name = None
        candidate_count = 0
        for artifact_name, artifact_spec in output_artifacts.items():
            if Stage.DEFAULT not in artifact_spec.stages and Stage.PREDICT not in artifact_spec.stages:
                continue

            if Stage.PREDICT in artifact_spec.stages:
                return artifact_name

            """
            Component like data split, three output_data, try to infer test
            """
            if "test" in artifact_name:
                return artifact_name

            candidate_artifact_name = artifact_name
            candidate_count += 1

        if candidate_count != 1:
            raise ValueError(f"Can not infer output artifact data name from {output_artifacts}")
        return candidate_artifact_name

    @classmethod
    def infer_test_input_data(cls,
                              train_artifact_definition,
                              test_artifact_definition,
                              channel: RuntimeTaskOutputChannelSpec,
                              dag_spec,
                              component_specs,
                              data_tracer: dict,
                              down_task_runtime_parties,
                              role,
                              party_id):
        if not (set(train_artifact_definition.types) & set(test_artifact_definition.types)):
            raise ValueError(f"train_artifact_definition's types are {train_artifact_definition.types[0]}, "
                             f"can not be changed to {test_artifact_definition.types[0]}")

        can_link_down = False
        for party_spec in down_task_runtime_parties:
            if party_spec.role == role and party_id in party_spec.party_id:
                can_link_down = True
                break

        if not can_link_down:
            return None

        if role not in data_tracer[channel.producer_task] or party_id not in data_tracer[channel.producer_task][role]:
            return None

        if role not in test_artifact_definition.roles or role not in train_artifact_definition.roles:
            return None

        parties = dag_spec.tasks[channel.producer_task].parties if dag_spec.tasks[channel.producer_task].parties else dag_spec.parties
        can_link_up = False
        for party_spec in parties:
            if role == party_spec.role and party_id in party_spec.party_id:
                can_link_up = True

        if not can_link_up:
            return None

        upstream_task = data_tracer[channel.producer_task][role][party_id]
        if not upstream_task:
            return None

        test_artifact_data_key = cls.infer_test_output_data_key(
            component_specs[upstream_task].output_artifacts.data
        )

        return [
            RuntimeTaskOutputChannelSpec(
                producer_task=upstream_task,
                output_artifact_key=test_artifact_data_key,
                parties=[PartySpec(role=role, party_id=[party_id])]
            )
        ]

    @classmethod
    def merge_artifact_channel_by_party(cls, channels: List[RuntimeTaskOutputChannelSpec]):
        channels.sort(key=lambda channel: (channel.producer_task, channel.output_artifact_key, channel.parties[0].role))
        merge_channels = []
        i = 0
        while i < len(channels):
            j = i + 1
            merge_channels.append(channels[i])
            while j < len(channels) and (channels[j].producer_task, channels[j].output_artifact_key) == \
                    (channels[i].producer_task, channels[i].output_artifact_key):
                if channels[j].parties[0].role == merge_channels[-1].parties[-1].role:
                    merge_channels[-1].parties[-1].party_id.append(channels[j].parties[-1].party_id[0])
                else:
                    merge_channels[-1].parties.append(channels[j].parties[0])

                j += 1

            i = j

        return merge_channels

    @classmethod
    def task_can_run(cls, role, party_id, component_spec: ComponentSpec=None, runtime_parties: List[PartySpec]=None):
        if component_spec and role not in component_spec.roles:
            return False

        for party_spec in runtime_parties:
            if role == party_spec.role and party_id in party_spec.party_id:
                return True

        return False

    @classmethod
    def trace_back_deploy_task(
            cls, task_name, task_name_set, dag_spec: DAGSpec,
            component_specs: Dict[str, ComponentSpec], data_tracer: dict,
            task_runtime_parties: Dict[str, List[PartySpec]], role, party_id):

        if task_name in task_name_set:
            if cls.task_can_run(role, party_id, component_specs[task_name], task_runtime_parties[task_name]):
                return task_name
            return None

        if task_name in data_tracer:
            if party_id in data_tracer[task_name].get(role, {}):
                return task_name
            return None

        task_spec = dag_spec.tasks[task_name]

        if task_spec.inputs is None or task_spec.inputs.data is None:
            return None

        for artifact_name, artifact_channel in task_spec.inputs.data.items():
            if not task_spec.stage:
                """
                task stage is train, inherit from job is train
                """
                if artifact_name == InputDataKeyType.VALIDATE_DATA:
                    continue

            for _, channel_list in artifact_channel.items():
                if not isinstance(channel_list, list):
                    channel_list = [channel_list]

                for channel in channel_list:
                    if isinstance(channel, DataWarehouseChannelSpec):
                        continue
                    assert isinstance(channel, RuntimeTaskOutputChannelSpec), f"channel={channel} not support to deploy"

                    producer_task = channel.producer_task
                    up_component_spec = component_specs[producer_task]
                    if not cls.task_can_run(role,
                                            party_id,
                                            up_component_spec,
                                            task_runtime_parties[task_name]):
                        continue

                    if not up_component_spec.output_artifacts or not up_component_spec.output_artifacts.data:
                        continue

                    test_output_data_key = cls.infer_test_output_data_key(up_component_spec.output_artifacts.data)
                    if role not in up_component_spec.output_artifacts.data[test_output_data_key].roles:
                        continue

                    if (up_input_name := cls.trace_back_deploy_task(
                                                producer_task,
                                                task_name_set,
                                                dag_spec,
                                                component_specs,
                                                data_tracer,
                                                task_runtime_parties,
                                                role,
                                                party_id)
                        ):
                        return up_input_name

        return None

    @classmethod
    def translate_dag(cls, src, dst, *args, **kwargs):
        from ..adapters import adapter_map
        translate_func = adapter_map[src][dst]

        return translate_func(*args, **kwargs)


class TaskNodeInfo(object):
    def __init__(self):
        self._runtime_parameters = None
        self._input_dependencies = None
        self._component_ref = None
        self._component_spec = None
        self._upstream_inputs = dict()
        self._outputs = dict()
        self._stage = None
        self._conf = None

    @property
    def stage(self):
        return self._stage

    @stage.setter
    def stage(self, stage):
        self._stage = stage

    @property
    def runtime_parameters(self):
        return self._runtime_parameters

    @runtime_parameters.setter
    def runtime_parameters(self, runtime_parameters):
        self._runtime_parameters = runtime_parameters

    @property
    def upstream_inputs(self):
        return self._upstream_inputs

    @upstream_inputs.setter
    def upstream_inputs(self, upstream_inputs):
        self._upstream_inputs = upstream_inputs

    @property
    def outputs(self):
        return self._outputs

    @outputs.setter
    def outputs(self, outputs):
        self._outputs = outputs

    @property
    def component_spec(self):
        return self._component_spec

    @component_spec.setter
    def component_spec(self, component_spec):
        self._component_spec = component_spec

    @property
    def output_definitions(self):
        return self._component_spec.output_definitions

    @property
    def component_ref(self):
        return self._component_ref

    @component_ref.setter
    def component_ref(self, component_ref):
        self._component_ref = component_ref

    @property
    def conf(self):
        return self._conf

    @conf.setter
    def conf(self, conf):
        self._conf = conf


class Party(BaseModel):
    role: str
    party_id: Union[str, int]
