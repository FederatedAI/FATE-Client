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
from ..utils.cli_utils import load_yaml, preprocess, prettify
from fate_client.flow_sdk import FlowClient


@click.group(short_help="FATE Flow Server Operations")
@click.pass_context
def table(ctx):
    """
    \b
    Provides numbers of component operational commands, including metrics, parameters and etc.
    For more details, please check out the help text.
    """
    pass


@table.command("query", short_help="Table query Command")
@cli_args.NAMESPACE_REQUIRED
@cli_args.NAME_REQUIRED
@cli_args.DISPLAY
@click.pass_context
def query(ctx, **kwargs):
    """
    - DESCRIPTION:


    \b
    - USAGE:
        flow table query --namespace $NAMESPACE --name xxx
    """
    client: FlowClient = ctx.obj["client"]
    response = client.table.query(**kwargs)
    prettify(response)


@table.command("delete", short_help="Table delete Command")
@cli_args.NAMESPACE_REQUIRED
@cli_args.NAME_REQUIRED
@click.pass_context
def delete(ctx, **kwargs):
    """
    - DESCRIPTION:


    \b
    - USAGE:
        flow table delete --namespace $NAMESPACE --name $TABLE_NAME
    """
    client: FlowClient = ctx.obj["client"]
    response = client.table.delete(**kwargs)
    prettify(response)

