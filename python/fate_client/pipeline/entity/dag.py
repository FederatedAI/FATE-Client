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

from .runtime_entity import PartySpec
from .dag_structures import RuntimeInputArtifacts, DAGSpec, DAGSchema, \
    TaskSpec, PartyTaskRefSpec, PartyTaskSpec, JobConfSpec
from ..scheduler.component_stage import ComponentStageSchedule

SCHEMA_VERSION = "2.1.0"


class DAG(object):
    def __init__(self):
        self._dag_spec = None
        self._is_compiled = False
        self._kind = "fate"

    @property
    def dag_spec(self):
        if not self._is_compiled:
            raise ValueError("Please compile pipeline first")

        return DAGSchema(dag=self._dag_spec, schema_version=SCHEMA_VERSION, kind=self._kind)

    def compile(self, parties, task_insts, stage, job_conf, protocol_kind):
        party_spec = parties.get_parties_spec()
        tasks = dict()
        party_tasks = dict()
        for task_name, task_inst in task_insts.items():
            task = dict(component_ref=task_inst.component_ref)
            dependent_tasks = task_inst.get_dependent_tasks()

            cpn_runtime_parties = task_inst.support_parties.get_party_inst_by_role(parties.get_runtime_roles())
            if not len(cpn_runtime_parties):
                cpn_runtime_parties = parties.get_party_inst_by_role(task_inst.support_roles)

            if cpn_runtime_parties != parties:
                task["parties"] = cpn_runtime_parties.get_parties_spec()

            input_channels, input_artifacts = task_inst.get_runtime_input_artifacts(cpn_runtime_parties)
            if task_inst.stage is None:
                task_stage = ComponentStageSchedule.get_stage(input_artifacts, default_stage='default')
            else:
                task_stage = task_inst.stage

            if input_channels:
                inputs = RuntimeInputArtifacts(**input_channels)
                task["inputs"] = inputs

            task["outputs"] = task_inst.get_output_artifacts()

            if dependent_tasks:
                task["dependent_tasks"] = dependent_tasks

            if task_inst.conf.dict():
                if "conf" not in task:
                    task["conf"] = dict()
                task["conf"].update(task_inst.conf.dict())

            common_parameters = task_inst.get_task_parameters()

            for role, party_id_list in cpn_runtime_parties:
                for idx, party_id in enumerate(party_id_list):
                    role_party_key = f"{role}_{party_id}"
                    role_parameters = task_inst.get_role_parameters(role, idx)
                    if role_parameters:
                        if role_party_key not in party_tasks:
                            party_tasks[role_party_key] = PartyTaskSpec(
                                parties=[PartySpec(role=role, party_id=[party_id])],
                                tasks=dict()
                            )

                        party_tasks[role_party_key].tasks[task_name] = PartyTaskRefSpec(
                            parameters=role_parameters
                        )

                    task_role_conf = task_inst.get_role_conf(role, idx)
                    if task_role_conf:
                        if role_party_key not in party_tasks:
                            party_tasks[role_party_key] = PartyTaskSpec(
                                parties=[PartySpec(role=role, party_id=[party_id])],
                                tasks=dict()
                            )

                        if task_name not in party_tasks[role_party_key].tasks:
                            party_tasks[role_party_key].tasks[task_name] = PartyTaskRefSpec(
                                conf=task_role_conf
                            )
                        else:
                            party_tasks[role_party_key].tasks[task_name].conf = task_role_conf

            if task_stage != stage:
                task["stage"] = task_stage
            task["parameters"] = common_parameters

            tasks[task_name] = TaskSpec(**task)

        self._dag_spec = DAGSpec(
            parties=party_spec,
            stage=stage,
            tasks=tasks
        )
        if job_conf.global_conf:
            self._dag_spec.conf = JobConfSpec(**job_conf.global_conf)

        if job_conf.parties_conf:
            for (role, party_id), party_conf in job_conf.parties_conf.items():
                party_key = f"{role}_{party_id}"
                if party_key in party_tasks:
                    party_tasks[party_key].conf = party_conf
                else:
                    party_tasks[party_key] = PartyTaskSpec(
                        conf=party_conf,
                        parties=[PartySpec(role=role, party_id=[party_id])]
                    )

        if party_tasks:
            self._dag_spec.party_tasks = party_tasks

        self._kind = protocol_kind
        self._is_compiled = True

        self._dag_spec = post_process(protocol_kind, self._dag_spec, task_insts)


def post_process(protocol_kind, pre_dag_spec: DAGSpec, task_insts):
    def _default_post_process(dag_spec: DAGSpec):
        post_dag_spec = copy.deepcopy(dag_spec)
        for task in post_dag_spec.tasks:
            if post_dag_spec.tasks[task].outputs:
                post_dag_spec.tasks[task].outputs = None

            if not post_dag_spec.tasks[task].conf:
                continue

        return post_dag_spec

    if protocol_kind == "fate":
        return _default_post_process(pre_dag_spec)
    else:
        try:
            from ..adapters import dag_post_process
            return dag_post_process[protocol_kind](pre_dag_spec, task_insts)
        except KeyError:
            return pre_dag_spec
