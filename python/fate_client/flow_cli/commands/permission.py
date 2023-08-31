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


@click.group()
@click.pass_context
def permission(ctx):
    """
    \b
    -description: Permission Operations
    """
    pass


@permission.command("grant")
@cli_args.APP_ID_REQUIRED
@cli_args.ROLE_REQUIRED
@click.pass_context
def grant(ctx, **kwargs):
    """
    \b
    -description: Grant permission


    \b
    -usage: flow permission grant --app-id xxx  -r xxx

    """
    client: FlowClient = ctx.obj["client"]
    response = client.permission.grant(**kwargs)
    prettify(response)


@permission.command("delete")
@cli_args.APP_ID_REQUIRED
@cli_args.ROLE_REQUIRED
@click.pass_context
def delete(ctx, **kwargs):
    """
    \b
    -description: Delete permission


    \b
    -usage: flow permission delete --app-id xxx --role client

    """
    client: FlowClient = ctx.obj["client"]
    response = client.permission.delete(**kwargs)
    prettify(response)


@permission.command("query")
@cli_args.APP_ID_REQUIRED
@click.pass_context
def query(ctx, **kwargs):
    """
    \b
    -description: Query permission


    \b
    -usage: flow permission query --app-id xxx

    """
    client: FlowClient = ctx.obj["client"]
    response = client.permission.query(**kwargs)
    prettify(response)


@permission.command("grant-resource")
@cli_args.CONF_PATH
@click.pass_context
def grant_resource(ctx, **kwargs):
    """
    \b
    -description: Granting Permissions to components, Datasets, etc.


    \b
    -usage: flow permission grant-resource -c examples/permission/grant.json

    """
    config_data = preprocess(**kwargs)
    client: FlowClient = ctx.obj["client"]
    response = client.permission.grant_resource(**config_data)
    prettify(response)


@permission.command("delete-resource")
@cli_args.CONF_PATH
@click.pass_context
def delete_resource(ctx, **kwargs):
    """
    \b
    -description: Delete Permissions of components, Datasets, etc.


    \b
    -usage: flow permission delete-resource -c examples/permission/delete.json

    """
    config_data = preprocess(**kwargs)
    client: FlowClient = ctx.obj["client"]
    response = client.permission.delete_resource(**config_data)
    prettify(response)


@permission.command("query-resource")
@cli_args.PARTYID_REQUIRED
@click.pass_context
def query_resource(ctx, **kwargs):
    """
    \b
    -description: Query Permissions of components, Datasets, etc.


    \b
    -usage: flow permission query-resource  -p 9999

    """
    client: FlowClient = ctx.obj["client"]
    response = client.permission.query_resource(**kwargs)
    prettify(response)
