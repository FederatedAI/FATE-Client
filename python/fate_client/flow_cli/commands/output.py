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


@click.group(short_help="Output Operations")
@click.pass_context
def output(ctx):
    """
    \b
    Provides numbers of data operational commands, including upload, download and etc.
    For more details, please check out the help text.
    """
    pass


@click.group(short_help="Output Data Operations")
@click.pass_context
def data(ctx):
    """
    \b
    Provides numbers of data operational commands, including upload, download and etc.
    For more details, please check out the help text.
    """
    pass


@output.command("key", short_help="Key metric query")
@cli_args.JOBID
@cli_args.ROLE
@cli_args.PARTYID
@click.pass_context
def query_key(ctx, **kwargs):
    """
    - DESCRIPTION:


    \b
    - USAGE:

    """
    # config_data, dsl_data = preprocess(**kwargs)
    client: FlowClient = ctx.obj["client"]
    response = client.output.query_metric_key(**kwargs)
    prettify(response)


@output.command("query", short_help="Metric query")
@cli_args.JOBID
@cli_args.ROLE
@cli_args.PARTYID
@cli_args.TASK_NAME
@click.pass_context
def query(ctx, **kwargs):
    """
    - DESCRIPTION:


    \b
    - USAGE:
        flow output query -j $JOB_ID -r guest -p 9999  -cpn reader_0

    """
    client: FlowClient = ctx.obj["client"]
    response = client.output.query_metric(**kwargs)
    prettify(response)


@output.command("delete", short_help="Metric delete")
@cli_args.JOBID
@cli_args.ROLE
@cli_args.PARTYID
@cli_args.TASK_NAME
@click.pass_context
def delete(ctx, **kwargs):
    """
    - DESCRIPTION:


    \b
    - USAGE:
        flow output delete -j $JOB_ID -r guest -p 9999  -cpn reader_0
    """
    client: FlowClient = ctx.obj["client"]
    response = client.output.delete_metric(**kwargs)
    prettify(response)


@output.command("m_query", short_help="Model query")
@cli_args.JOBID
@cli_args.ROLE
@cli_args.PARTYID
@cli_args.TASK_NAME
@click.pass_context
def query(ctx, **kwargs):
    """
    - DESCRIPTION:


    \b
    - USAGE:
        flow output m_query -j $JOB_ID -r guest -p 9999  -cpn reader_0
    """
    client: FlowClient = ctx.obj["client"]
    response = client.output.query_model(**kwargs)
    prettify(response)


@output.command("m_delete", short_help="Model delete")
@cli_args.JOBID
@cli_args.ROLE
@cli_args.PARTYID
@cli_args.TASK_NAME
@click.pass_context
def delete(ctx, **kwargs):
    """
    - DESCRIPTION:


    \b
    - USAGE:
        flow output m_qdelete -j $JOB_ID -r guest -p 9999  -cpn reader_0
    """
    client: FlowClient = ctx.obj["client"]
    response = client.output.delete_model(**kwargs)
    prettify(response)


@data.command("download", short_help="Download data")
@cli_args.JOBID
@cli_args.ROLE
@cli_args.PARTYID
@cli_args.TASK_NAME
@click.pass_context
def download_data(ctx, **kwargs):
    """
    - DESCRIPTION:


    \b
    - USAGE:
        flow output m_qdelete -j $JOB_ID -r guest -p 9999  -cpn reader_0
    """
    client: FlowClient = ctx.obj["client"]
    response = client.output.download_data(**kwargs)
    prettify(response)