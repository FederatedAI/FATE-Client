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


@click.group()
@click.pass_context
def table(ctx):
    """
    \b
    -description: Data Table Operations, such as Querying and Deleting, and more
    """
    pass


@table.command("query")
@cli_args.NAMESPACE_REQUIRED
@cli_args.NAME_REQUIRED
@cli_args.DISPLAY
@click.pass_context
def query(ctx, **kwargs):
    """
    \b
    -description: Query data table.

    \b
    -usage: flow table query --name xxx --namespace xxx
    """
    client: FlowClient = ctx.obj["client"]
    response = client.table.query(**kwargs)
    prettify(response)


@table.command("delete")
@cli_args.NAMESPACE_REQUIRED
@cli_args.NAME_REQUIRED
@click.pass_context
def delete(ctx, **kwargs):
    """
    \b
    -description: Delete data table.

    \b
    -usage: flow table delete --name xxx --namespace xxx
    """
    client: FlowClient = ctx.obj["client"]
    response = client.table.delete(**kwargs)
    prettify(response)

