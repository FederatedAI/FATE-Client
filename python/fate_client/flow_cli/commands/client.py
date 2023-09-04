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
def client(ctx):
    """
    \b
    -description: Client Operations
    """
    pass


@client.command("create-client")
@cli_args.APP_NAME_REQUIRED
@click.pass_context
def create_client(ctx, **kwargs):
    """
    \b
    -description: Create a client

    \b
    -usage: flow client create-client --app-name xxx
    """
    client: FlowClient = ctx.obj["client"]
    response = client.client_.create_client(**kwargs)
    prettify(response)


@client.command("delete-client")
@cli_args.APP_ID_REQUIRED
@click.pass_context
def delete_client(ctx, **kwargs):
    """
    \b
    -description: Delete a client

    \b
    -usage: flow client delete-client --app-id xxx
    """
    client: FlowClient = ctx.obj["client"]
    response = client.client_.delete_client(**kwargs)
    prettify(response)


@client.command("query-client")
@cli_args.APP_ID
@cli_args.APP_NAME
@click.pass_context
def query_client(ctx, **kwargs):
    """
    \b
    -description: Querying Client Information by Filtering Conditions

    \b
    -usage: flow client query-client  --app-id xxx --app-name xxx
    """
    client: FlowClient = ctx.obj["client"]
    response = client.client_.query_client(**kwargs)
    prettify(response)


@client.command("create-site")
@cli_args.PARTYID_REQUIRED
@click.pass_context
def create_site(ctx, **kwargs):
    """
    \b
    -description: Create partner site

    \b
    -usage: flow client create-site -p xxx
    """
    client: FlowClient = ctx.obj["client"]
    response = client.client_.create_site(**kwargs)
    prettify(response)


@client.command("delete-site")
@cli_args.PARTYID_REQUIRED
@click.pass_context
def delete_site(ctx, **kwargs):
    """
    \b
    -description: Delete partner site

    \b
    -usage: flow client delete-site -p xxx
    """
    client: FlowClient = ctx.obj["client"]
    response = client.client_.delete_site(**kwargs)
    prettify(response)


@client.command("query-site")
@cli_args.PARTYID_REQUIRED
@click.pass_context
def query_site(ctx, **kwargs):
    """
    \b
    -description: Query partner site

    \b
    -usage: flow client query-site -p xxx
    """
    client: FlowClient = ctx.obj["client"]
    response = client.client_.query_site(**kwargs)
    prettify(response)


@client.command("create-partner")
@cli_args.PARTYID_REQUIRED
@cli_args.APP_ID_REQUIRED
@cli_args.APP_TOKEN_REQUIRED
@click.pass_context
def create_partner(ctx, **kwargs):
    """
    \b
    -description: Establishing Partnership with a Site

    \b
    -usage: flow client create-partner -p xxx --app-id xxx --app-token xxx
    """
    client: FlowClient = ctx.obj["client"]
    response = client.client_.create_partner(**kwargs)
    prettify(response)


@client.command("delete-partner")
@cli_args.PARTYID_REQUIRED
@click.pass_context
def delete_partner(ctx, **kwargs):
    """
    \b
    -description: Disassociating Partnership with a Site.

    \b
    -usage: flow client delete-partner -p xxx
    """
    client: FlowClient = ctx.obj["client"]
    response = client.client_.delete_partner(**kwargs)
    prettify(response)


@client.command("query-partner")
@cli_args.PARTYID
@click.pass_context
def query_partner(ctx, **kwargs):
    """
    \b
    -description: Querying Sites with Established Partnerships.

    \b
    -usage: flow client query-partner -p xxx
    """
    client: FlowClient = ctx.obj["client"]
    response = client.client_.query_partner(**kwargs)
    prettify(response)
