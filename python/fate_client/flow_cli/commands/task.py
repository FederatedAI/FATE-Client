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
from ..utils.cli_utils import prettify
from fate_client.flow_sdk import FlowClient


@click.group()
@click.pass_context
def task(ctx):
    """
    \b
    -description: Provides numbers of task operational commands, including list and query. For more details, please check out the help text.
    """
    pass


@task.command("query")
@cli_args.JOBID
@cli_args.ROLE_IDE
@cli_args.PARTYID
@cli_args.TASK_NAME
@cli_args.STATUS
@cli_args.TASK_ID
@cli_args.TASK_VERSION
@click.pass_context
def query(ctx, **kwargs):
    """
    \b
    -description: Querying Tasks by Filtering Conditions.

    \b
    -usage: flow task query -j xxx -r guest -p 9999 -tn xxx
    """
    client: FlowClient = ctx.obj["client"]
    response = client.task.query(**kwargs)
    prettify(response)


@task.command("list")
@cli_args.JOBID
@cli_args.ROLE_IDE
@cli_args.PARTYID
@cli_args.TASK_NAME
@cli_args.LIMIT
@click.pass_context
def query_list(ctx, **kwargs):
    """
    \b
    -description: Fetching Task List by Filtering Conditions.

    \b
    -usage: flow task list -j xxx -r guest -p 9999
    """
    client: FlowClient = ctx.obj["client"]
    response = client.task.query_task_list(**kwargs)
    prettify(response)


