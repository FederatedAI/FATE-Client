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
from ruamel import yaml
from .executor import FateFlowExecutor
from .entity import DAG
from .entity.dag_structures import JobConfSpec, ModelWarehouseConfSpec
from .entity import FateFlowTaskInfo
from .entity.runtime_entity import Roles
from .conf.env_config import SiteInfo
from .conf.types import SupportRole, PlaceHolder, InputArtifactType
from .conf.job_configuration import JobConf
from .components.component_base import Component
from .scheduler.dag_parser import DagParser


class Pipeline(object):
    def __init__(self, executor, *args):
        self._executor = executor
        self._dag = DAG()
        self._roles = Roles()
        self._stage = "train"
        self._tasks = dict()
        self._job_conf = JobConf()
        self._model_info = None
        self._predict_dag = None
        self._local_role = SiteInfo.ROLE
        self._local_party_id = SiteInfo.PARTY_ID

    def set_site_role(self, role):
        self._local_role = role
        return self

    def set_site_party_id(self, party_id):
        self._local_party_id = party_id
        return self

    def set_stage(self, stage):
        self._stage = stage
        return self

    @property
    def conf(self):
        return self._job_conf

    @conf.setter
    def conf(self, job_conf):
        self._job_conf = job_conf

    @property
    def model_info(self):
        return self._model_info

    @model_info.setter
    def model_info(self, model_info):
        self._model_info = model_info

    @property
    def predict_dag(self):
        return self._predict_dag

    @property
    def stage(self):
        return self._stage

    @predict_dag.setter
    def predict_dag(self, predict_dag):
        self._predict_dag = predict_dag

    @property
    def tasks(self):
        return self._tasks

    def set_roles(self, guest=None, host=None, arbiter=None, **kwargs):
        local_vars = locals()
        local_vars.pop("kwargs")
        if kwargs:
            local_vars.update(kwargs)

        support_roles = SupportRole.support_roles()
        for role, party_id in local_vars.items():
            if role == "self" or party_id is None:
                continue

            if role not in support_roles:
                raise ValueError(f"role {role} is not support")

            if isinstance(party_id, int):
                party_id = str(party_id)
            elif isinstance(party_id, list):
                party_id = [str(_id) for _id in party_id]
            self._roles.set_role(role, party_id)

        return self

    @property
    def roles(self) -> Roles:
        return self._roles

    @roles.setter
    def roles(self, roles):
        self._roles = roles

    def add_task(self, task) -> "Pipeline":
        if isinstance(task, Component):
            if task.task_name in self._tasks:
                raise ValueError(f"Task {task.task_name} has been added before")

            self._tasks[task.task_name] = task
        elif isinstance(task, Pipeline):
            if task.stage != "deployed":
                raise ValueError("Deploy training pipeline first and use get_deployed_pipeline to get the inst")

            self._stage = "predict"
            if not self._roles.is_initialized():
                self._roles = task.roles

            self._tasks.update(task.tasks)
            self._job_conf.update(task.conf.dict())
            self._model_info = task.model_info

        return self

    def compile(self) -> "Pipeline":
        self._dag.compile(task_insts=self._tasks,
                          roles=self._roles,
                          stage=self._stage,
                          job_conf=self._job_conf.dict())
        return self

    def get_deployed_pipeline(self):
        if not self._predict_dag:
            raise ValueError("To get deployed pipeline, deploy first")

        deploy_pipeline = Pipeline(self._executor)
        deploy_pipeline.set_stage("deployed")
        deploy_pipeline.conf = self._job_conf
        if self._predict_dag.conf:
            deploy_pipeline.conf.update(self._predict_dag.conf.dict(exclude_defaults=True))
        deploy_pipeline.predict_dag = self._predict_dag
        deploy_pipeline.roles = self._roles
        deploy_pipeline.model_info = self._model_info

        for task_name, task in self._tasks.items():
            if task_name not in self._predict_dag.tasks:
                continue
            deploy_task = copy.deepcopy(task)
            predict_task_spec = self._predict_dag.tasks[task_name]
            for artifact_type in InputArtifactType.types():
                if not getattr(task.component_spec.input_artifacts, artifact_type):
                    continue
                artifacts = getattr(task.component_spec.input_artifacts, artifact_type)
                input_artifact_keys = artifacts.keys()
                for input_artifact_key in input_artifact_keys:
                    setattr(deploy_task, input_artifact_key, PlaceHolder())

                if not predict_task_spec.inputs or not getattr(predict_task_spec.inputs, artifact_type):
                    continue
                artifacts = getattr(predict_task_spec.inputs, artifact_type)
                for input_artifact_key, input_channel in artifacts.items():
                    for artifact_source_type, channel in input_channel.items():
                        channels = channel if isinstance(channel, list) else [channel]
                        changed_channels = []
                        for _c in channels:
                            producer_task = _c.producer_task
                            output_artifact_key = _c.output_artifact_key
                            changed_channel = copy.deepcopy(self._tasks[producer_task].outputs[output_artifact_key])
                            changed_channel.source = artifact_source_type
                            changed_channels.append(changed_channel)

                        if isinstance(channel, list):
                            setattr(deploy_task, input_artifact_key, changed_channels)
                        else:
                            setattr(deploy_task, input_artifact_key, changed_channels[0])

            deploy_pipeline.add_task(deploy_task)

        party_tasks = self._dag.dag_spec.dag.party_tasks
        if not party_tasks:
            return deploy_pipeline

        for site_name, party_task_spec in party_tasks.items():
            if not party_task_spec.tasks:
                continue

            for task_name, task_spec in party_task_spec.tasks.items():
                if task_spec.inputs:
                    try:
                        getattr(deploy_pipeline, task_name).reset_source_inputs()
                    except AttributeError:
                        pass

        return deploy_pipeline

    def get_dag(self):
        return yaml.safe_dump(self._dag.dag_spec.dict(exclude_defaults=True))

    def get_component_specs(self):
        component_specs = dict()
        for task_name, task in self._tasks.items():
            component_specs[task_name] = task.component_spec

        return component_specs

    def get_task_info(self, task_name):
        raise NotADirectoryError

    def fit(self) -> "Pipeline":
        self._model_info = self._executor.fit(self._dag.dag_spec,
                                              self.get_component_specs(),
                                              local_role=self._local_role,
                                              local_party_id=self._local_party_id)

        return self

    def predict(self) -> "Pipeline":
        self._model_info = self._executor.predict(self._dag.dag_spec,
                                                  self.get_component_specs(),
                                                  self._model_info)

        return self

    def deploy(self, task_list=None):
        """
        this will return predict dag IR
        if component_list is None: deploy all
        """
        if self._stage != "train":
            raise ValueError(f"Only training pipeline can be deployed, but this pipeline's stage is {self._stage}")

        if task_list:
            task_name_list = []
            for task in task_list:
                if isinstance(task, Component):
                    task_name_list.append(task.task_name)
                else:
                    task_name_list.append(task)
        else:
            task_name_list = [task.name for (task_name, task) in self._tasks.items()]

        self._predict_dag = DagParser.deploy(task_name_list, self._dag.dag_spec, self.get_component_specs())

        if self._model_info:
            if self._predict_dag.conf is None:
                self._predict_dag.conf = JobConfSpec()
            self._predict_dag.conf.model_warehouse = ModelWarehouseConfSpec(model_id=self._model_info.model_id,
                                                                            model_version=self._model_info.model_version)

        return yaml.dump(self._predict_dag.dict(exclude_defaults=True))

    def __getattr__(self, attr):
        if attr in self._tasks:
            return self._tasks[attr]

        return self.__getattribute__(attr)

    def __getitem__(self, item):
        if item not in self._tasks:
            raise ValueError(f"Component {item} has not been added in pipeline")

        return self._tasks[item]


class FateFlowPipeline(Pipeline):
    def __init__(self, *args):
        super(FateFlowPipeline, self).__init__(FateFlowExecutor(), *args)

    def transform_local_file_to_dataframe(self,
                                          file: str,
                                          head: str,
                                          namespace: str,
                                          name: str,
                                          meta: dict,
                                          extend_sid=True,
                                          partitions=4,
                                          site_name: str = None,
                                          **kwargs):
        data_warehouse = self._executor.upload(file=file,
                                               head=head,
                                               meta=meta,
                                               partitions=partitions,
                                               extend_sid=extend_sid,
                                               role="local",
                                               party_id="0",
                                               **kwargs)
        self._executor.transform_to_dataframe(namespace, name, data_warehouse, site_name=site_name, role="local", party_id="0")

    def get_task_info(self, task):
        if isinstance(task, Component):
            task = task.task_name

        if task not in self._tasks:
            raise ValueError(f"Task {task} not exist")

        return FateFlowTaskInfo(task_name=task, model_info=self._model_info)
