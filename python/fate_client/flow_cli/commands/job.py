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
import click

from ..utils import cli_args
from ..utils.cli_utils import load_yaml


from fate_client.flow_sdk import FlowClient


@click.group(short_help="Job Operations")
@click.pass_context
def job(ctx):
    """
    \b
    Provides numbers of job operational commands, including submit, stop, query and etc.
    For more details, please check out the help text.
    """
    pass


@job.command("submit", short_help="Submit Job Command")
@cli_args.CONF_PATH
@click.pass_context
def submit(ctx, **kwargs):
    """
    - DESCRIPTION:

    \b
    Submit a pipeline job.
    Used to be 'submit_job'.

    \b
    - USAGE:
        flow job submit -c fate_flow/examples/lr/standalone/lr_train_dag.yaml
    """
    dag_schema = load_yaml(kwargs.get("config_path"))
    client: FlowClient = ctx.obj[["client"]]
    return client.job.submit(dag_schema=dag_schema)
