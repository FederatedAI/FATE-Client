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
from pathlib import Path
from typing import Dict
from ..entity.dag_structures import DAGSchema
from ..entity.component_structures import ComponentSpec
from ..utils.fateflow.fate_flow_job_invoker import FATEFlowJobInvoker
from ..utils.callbacks import CallbackHandler
from ..entity.model_info import FateFlowModelInfo


class FateFlowExecutor(object):
    def __init__(self):
        ...

    def fit(self, dag_schema: DAGSchema, component_specs: Dict[str, ComponentSpec],
            local_role: str, local_party_id: str, callback_handler: CallbackHandler) -> FateFlowModelInfo:
        flow_job_invoker = FATEFlowJobInvoker()
        local_party_id = self.get_site_party_id(flow_job_invoker, dag_schema, local_role, local_party_id)

        return self._run(
            dag_schema,
            local_role,
            local_party_id,
            flow_job_invoker,
            callback_handler,
            event="fit"
        )

    def predict(self,
                dag_schema: DAGSchema,
                component_specs: Dict[str, ComponentSpec],
                fit_model_info: FateFlowModelInfo, callback_handler: CallbackHandler) -> FateFlowModelInfo:
        flow_job_invoker = FATEFlowJobInvoker()
        schedule_role = fit_model_info.local_role
        schedule_party_id = fit_model_info.local_party_id

        return self._run(
            dag_schema,
            schedule_role,
            schedule_party_id,
            flow_job_invoker,
            callback_handler,
            event="predict"
        )

    def _run(self,
             dag_schema: DAGSchema,
             local_role,
             local_party_id,
             flow_job_invoker: FATEFlowJobInvoker,
             callback_handler: CallbackHandler,
             event="fit") -> FateFlowModelInfo:

        job_id, model_id, model_version = flow_job_invoker.submit_job(dag_schema.dict(exclude_defaults=True))

        getattr(callback_handler, f"on_{event}_begin")(
            job_info=dict(
                job_id=job_id,
                model_id=model_id,
                model_version=model_version
            )
        )

        flow_job_invoker.monitor_status(job_id, local_role, local_party_id)

        getattr(callback_handler, f"on_{event}_end")(
            job_info=dict(
                job_id=job_id,
                model_id=model_id,
                model_version=model_version
            )
        )

        return FateFlowModelInfo(
            job_id=job_id,
            local_role=local_role,
            local_party_id=local_party_id,
            model_id=model_id,
            model_version=model_version
        )

    @staticmethod
    def get_site_party_id(flow_job_invoker, dag_schema, role, party_id):
        site_party_id = flow_job_invoker.query_site_info()

        if site_party_id:
            return site_party_id

        if party_id:
            return party_id

        if site_party_id is None:
            for party in dag_schema.dag.parties:
                if role == party.role:
                    return party.party_id[0]

        raise ValueError(f"Can not retrieval site's party_id from site's role {role}")

    @staticmethod
    def upload(file: str,
               head: bool,
               meta: dict,
               role,
               party_id,
               namespace,
               name,
               extend_sid=True,
               partitions=4,
               **kwargs):
        flow_job_invoker = FATEFlowJobInvoker()

        return flow_job_invoker.upload_file_and_convert_to_dataframe(
            file=file,
            head=head,
            meta=meta,
            extend_sid=extend_sid,
            partitions=partitions,
            role=role,
            party_id=party_id,
            namespace=namespace,
            name=name,
            **kwargs)

    @staticmethod
    def bind_local_path(path: str, namespace: str, name: str):
        flow_job_invoker = FATEFlowJobInvoker()
        return flow_job_invoker.bind_local_path(path=path, namespace=namespace, name=name)

