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
from ..utils.cli_utils import preprocess,prettify
from fate_client.flow_sdk import FlowClient


@click.group(short_help="Log Operations")
@click.pass_context
def log(ctx):
    """
    \b
    Provides numbers of data operational commands, including upload, download and etc.
    For more details, please check out the help text.
    """
    pass


@log.command("count", short_help="Count Log Command")
@cli_args.LOG_TYPE_REQUIRED
@cli_args.JOBID_REQUIRED
@cli_args.ROLE
@cli_args.PARTYID
@cli_args.TABLE_NAME
@cli_args.INSTANCE_ID
@click.pass_context
def count(ctx, **kwargs):
    """
    - DESCRIPTION:

    \b
    - USAGE:
        flow log count --log-type xxx -j xx

    """
    client: FlowClient = ctx.obj["client"]
    response = client.log.count(**kwargs)
    prettify(response)


@log.command("query", short_help="Log query Command")
@cli_args.LOG_TYPE_REQUIRED
@cli_args.JOBID_REQUIRED
@cli_args.ROLE_IDE
@cli_args.PARTYID
@cli_args.TASK_NAME
@cli_args.INSTANCE_ID
@click.pass_context
def query(ctx, **kwargs):
    """
    - DESCRIPTION:
        Query Log.

    \b
    - USAGE:
        flow log query --log-type xxx -j $JOBID
    """
    client: FlowClient = ctx.obj["client"]
    response = client.log.query(**kwargs)
    prettify(response)




