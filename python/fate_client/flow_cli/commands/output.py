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


@output.command("key", short_help="Key metric query")
@cli_args.JOBID_REQUIRED
@cli_args.ROLE_IDE_REQUIRED
@cli_args.PARTYID_REQUIRED
@cli_args.TASK_NAME_REQUIRED
@click.pass_context
def query_key(ctx, **kwargs):
    """
    - DESCRIPTION:


    \b
    - USAGE:
        flow output key -j $JOB_ID -r guest -p 9999  -tn reader_0

    """
    client: FlowClient = ctx.obj["client"]
    response = client.output.query_metric_key(**kwargs)
    prettify(response)


@output.command("query-metric", short_help="Metric query")
@cli_args.JOBID_REQUIRED
@cli_args.ROLE_IDE_REQUIRED
@cli_args.PARTYID_REQUIRED
@cli_args.TASK_NAME_REQUIRED
@click.pass_context
def query_metric(ctx, **kwargs):
    """
    - DESCRIPTION:


    \b
    - USAGE:
        flow output query-metric -j $JOB_ID -r guest -p 9999  -tn reader_0

    """
    client: FlowClient = ctx.obj["client"]
    response = client.output.query_metric(**kwargs)
    prettify(response)


@output.command("delete-metric", short_help="Metric delete")
@cli_args.JOBID_REQUIRED
@cli_args.ROLE_IDE_REQUIRED
@cli_args.PARTYID_REQUIRED
@cli_args.TASK_NAME_REQUIRED
@click.pass_context
def delete_metric(ctx, **kwargs):
    """
    - DESCRIPTION:
        delete metric.
        Used to be 'delete-metric'.
    \b
    - USAGE:
        flow output delete-metric -j $JOB_ID -r guest -p 9999  -tn reader_0

    """
    client: FlowClient = ctx.obj["client"]
    response = client.output.delete_metric(**kwargs)
    prettify(response)


@output.command("query-model", short_help="Model query")
@cli_args.JOBID_REQUIRED
@cli_args.ROLE_IDE_REQUIRED
@cli_args.PARTYID_REQUIRED
@cli_args.TASK_NAME_REQUIRED
@click.pass_context
def query_model(ctx, **kwargs):
    """
    - DESCRIPTION:

    \b
    - USAGE:
        flow output query-model -j $JOB_ID -r guest -p 9999  -tn reader_0

    """
    client: FlowClient = ctx.obj["client"]
    response = client.output.query_model(**kwargs)
    prettify(response)


@output.command("down-model", short_help="Model Down")
@cli_args.JOBID_REQUIRED
@cli_args.ROLE_IDE_REQUIRED
@cli_args.PARTYID_REQUIRED
@cli_args.TASK_NAME_REQUIRED
@cli_args.PATH_REQUIRED
@click.pass_context
def down_model(ctx, **kwargs):
    """
    - DESCRIPTION:

    \b
    - USAGE:
        flow output down-model -j $JOB_ID -r guest -p 9999  -tn reader_0 -o /data/project/xxx

    """
    client: FlowClient = ctx.obj["client"]
    response = client.output.down_model(**kwargs)
    prettify(response)


@output.command("delete-model", short_help="Model delete")
@cli_args.JOBID_REQUIRED
@cli_args.ROLE_IDE_REQUIRED
@cli_args.PARTYID_REQUIRED
@cli_args.TASK_NAME_REQUIRED
@click.pass_context
def delete_model(ctx, **kwargs):
    """
    - DESCRIPTION:

    \b
    - USAGE:
        flow output delete-model -j $JOB_ID -r guest -p 9999  -tn reader_0

    """
    client: FlowClient = ctx.obj["client"]
    response = client.output.delete_model(**kwargs)
    prettify(response)


@output.command("download", short_help="Download data")
@cli_args.JOBID_REQUIRED
@cli_args.ROLE_IDE_REQUIRED
@cli_args.PARTYID_REQUIRED
@cli_args.TASK_NAME_REQUIRED
@cli_args.PATH
@click.pass_context
def download_data(ctx, **kwargs):
    """
    - DESCRIPTION:

    \b
    - USAGE:
        flow output download -j $JOB_ID -r guest -p 9999  -tn reader_0  -o /data/project/xx

    """
    client: FlowClient = ctx.obj["client"]
    response = client.output.download_data(**kwargs)
    prettify(response)


@output.command("table", short_help="Get data table")
@cli_args.JOBID_REQUIRED
@cli_args.ROLE_IDE_REQUIRED
@cli_args.PARTYID_REQUIRED
@cli_args.TASK_NAME_REQUIRED
@click.pass_context
def table_data(ctx, **kwargs):
    """
    - DESCRIPTION:

    \b
    - USAGE:
        flow output table -j $JOB_ID -r guest -p 9999  -tn reader_0

    """
    client: FlowClient = ctx.obj["client"]
    response = client.output.data_table(**kwargs)
    prettify(response)


@output.command("display", short_help="Display data")
@cli_args.JOBID_REQUIRED
@cli_args.ROLE_IDE_REQUIRED
@cli_args.PARTYID_REQUIRED
@cli_args.TASK_NAME_REQUIRED
@click.pass_context
def display_data(ctx, **kwargs):
    """
    - DESCRIPTION:

    \b
    - USAGE:
        flow output display -j $JOB_ID -r guest -p 9999  -tn reader_0

    """
    client: FlowClient = ctx.obj["client"]
    response = client.output.data_display(**kwargs)
    prettify(response)
