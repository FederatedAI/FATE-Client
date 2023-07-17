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


@click.group(short_help="Client Operations")
@click.pass_context
def client(ctx):
    """
    \b
    Provides numbers of client operational commands, including create, delete, query and etc.
    For more details, please check out the help text.
    """
    pass


@client.command("create-client", short_help="Create Client Command")
@cli_args.APP_NAME
@click.pass_context
def create_client(ctx, **kwargs):
    """
    - DESCRIPTION:

    \b
    Create client.
    Used to be 'create client'.

    \b
    - USAGE:
        flow client create-client -app_name xxx
    """
    client: FlowClient = ctx.obj["client"]
    response = client.client_.create_client(**kwargs)
    prettify(response)


@client.command("delete-client", short_help="Delete Client Command")
@cli_args.APP_ID
@click.pass_context
def delete_client(ctx, **kwargs):
    """
    - DESCRIPTION:

    \b
    Delete client.
    Used to be 'delete client'.

    \b
    - USAGE:
        flow client delete-client -app_id xxx
    """
    client: FlowClient = ctx.obj["client"]
    response = client.client_.delete_client(**kwargs)
    prettify(response)


@client.command("query-client", short_help="Query Client Command")
@cli_args.APP_ID
@cli_args.APP_NAME
@click.pass_context
def query_client(ctx, **kwargs):
    """
    - DESCRIPTION:

    \b
    Query client.
    Used to be 'query client'.

    \b
    - USAGE:
        flow client query-client  -app_id xxx -app_name xxx
    """
    client: FlowClient = ctx.obj["client"]
    response = client.client_.query_client(**kwargs)
    prettify(response)


@client.command("create-site", short_help="Create Site Command")
@cli_args.PARTYID
@click.pass_context
def create_site(ctx, **kwargs):
    """
    - DESCRIPTION:

    \b
    Create site.
    Used to be 'create site'.

    \b
    - USAGE:
        flow client create-site -p xxx
    """
    client: FlowClient = ctx.obj["client"]
    response = client.client_.create_site(**kwargs)
    prettify(response)


@client.command("delete-site", short_help="Delete Site Command")
@cli_args.PARTYID
@click.pass_context
def delete_site(ctx, **kwargs):
    """
    - DESCRIPTION:

    \b
    Delete site.
    Used to be 'delete site'.

    \b
    - USAGE:
        flow client delete-site -p xxx
    """
    client: FlowClient = ctx.obj["client"]
    response = client.client_.delete_site(**kwargs)
    prettify(response)


@client.command("query-site", short_help="Query Site Command")
@cli_args.PARTYID
@click.pass_context
def query_site(ctx, **kwargs):
    """
    - DESCRIPTION:

    \b
    Query site.
    Used to be 'query site'.

    \b
    - USAGE:
        flow client query-site -p xxx
    """
    client: FlowClient = ctx.obj["client"]
    response = client.client_.query_site(**kwargs)
    prettify(response)


@client.command("create-partner", short_help="Create Partner Command")
@cli_args.PARTYID
@cli_args.APP_ID
@cli_args.APP_TOKEN
@click.pass_context
def create_partner(ctx, **kwargs):
    """
    - DESCRIPTION:

    \b
    Create partner.
    Used to be 'create partner'.

    \b
    - USAGE:
        flow create create-partner -p xxx
    """
    client: FlowClient = ctx.obj["client"]
    response = client.client_.create_partner(**kwargs)
    prettify(response)


@client.command("delete-partner", short_help="Delete Partner Command")
@cli_args.PARTYID
@click.pass_context
def delete_partner(ctx, **kwargs):
    """
    - DESCRIPTION:

    \b
    Delete partner.
    Used to be 'delete partner'.

    \b
    - USAGE:
        flow client delete-partner -p xxx
    """
    client: FlowClient = ctx.obj["client"]
    response = client.client_.delete_partner(**kwargs)
    prettify(response)


@client.command("query-partner", short_help="Query Partner Command")
@cli_args.PARTYID
@click.pass_context
def query_partner(ctx, **kwargs):
    """
    - DESCRIPTION:

    \b
    Query site.
    Used to be 'query partner'.

    \b
    - USAGE:
        flow client query-partner -p xxx
    """
    client: FlowClient = ctx.obj["client"]
    response = client.client_.query_partner(**kwargs)
    prettify(response)