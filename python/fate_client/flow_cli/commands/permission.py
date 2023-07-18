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

from fate_client.flow_sdk import FlowClient
from ..utils import cli_args
from ..utils.cli_utils import load_yaml, preprocess, prettify


@click.group(short_help="Permission Operations")
@click.pass_context
def permission(ctx):
    """
    \b
    Provides numbers of data operational commands, including upload, download and etc.
    For more details, please check out the help text.
    """
    pass


@permission.command("grant", short_help="Grant permission Command")
@cli_args.APP_ID_REQUIRED
@cli_args.ROLE_REQUIRED
@click.pass_context
def grant(ctx, **kwargs):
    """
    - DESCRIPTION:


    \b
    grant component | dataset privilege

    \b
    - USAGE:
        flow permission grant -app_id $APP_ID  -r site
    """
    client: FlowClient = ctx.obj["client"]
    response = client.permission.grant(**kwargs)
    prettify(response)


@permission.command("delete", short_help="Delete Privilege Command")
@cli_args.APP_ID_REQUIRED
@cli_args.ROLE_REQUIRED
@click.pass_context
def delete(ctx, **kwargs):
    """
    - DESCRIPTION:


    \b
    delete component | dataset privilege

    \b
    - USAGE:
        flow permission delete  -app_id $APP_ID  -r site
    """
    client: FlowClient = ctx.obj["client"]
    response = client.permission.delete(**kwargs)
    prettify(response)


@permission.command("query", short_help="Query Privilege Command")
@cli_args.APP_ID_REQUIRED
@click.pass_context
def query(ctx, **kwargs):
    """
    - DESCRIPTION:


    \b
    query component | dataset privilege

    \b
    - USAGE:
        flow permission query  -app_id $APP_ID
    """
    client: FlowClient = ctx.obj["client"]
    response = client.permission.query(**kwargs)
    prettify(response)
