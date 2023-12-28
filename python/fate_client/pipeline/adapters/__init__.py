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

from .bfia.translator.dsl_translator import Translator

def _default_dag_post_process_func(dag_spec, task_insts):
    task_names = dag_spec.tasks.keys()
    for task_name in task_names:
        provider = task_insts[task_name].provider
        version = task_insts[task_name].version
        if not dag_spec.tasks[task_name].conf:
            dag_spec.tasks[task_name].conf = dict()
        dag_spec.tasks[task_name].conf.update(dict(provider=provider, version=version))

    return dag_spec


adapter_map = {
    "fate": {
        "bfia": Translator.translate_dag_to_bfia_dag
    },
    "bfia": {
        "fate": Translator.translate_bfia_dag_to_dag
    }
}

dag_post_process = {
    "bfia": _default_dag_post_process_func
}