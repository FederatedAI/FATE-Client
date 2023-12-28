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
def output(ctx):
    """
    \b
    -description: Task output Operations
    """
    pass


@output.command("query-metric-key")
@cli_args.JOBID_REQUIRED
@cli_args.ROLE_IDE_REQUIRED
@cli_args.PARTYID_REQUIRED
@cli_args.TASK_NAME_REQUIRED
@click.pass_context
def query_key(ctx, **kwargs):
    """
    \b
    -description: Query metric key


    \b
    -usage: flow output query-metric-key -j xxx -r guest -p 9999 -tn lr_0

    """
    client: FlowClient = ctx.obj["client"]
    response = client.output.query_metric_key(**kwargs)
    prettify(response)


@output.command("query-metric")
@cli_args.JOBID_REQUIRED
@cli_args.ROLE_IDE_REQUIRED
@cli_args.PARTYID_REQUIRED
@cli_args.TASK_NAME_REQUIRED
@click.pass_context
def query_metric(ctx, **kwargs):
    """
    \b
    -description: Query metric


    \b
    -usage: flow output query-metric -j xxx -r guest -p 9999 -tn lr_0

    """
    client: FlowClient = ctx.obj["client"]
    response = client.output.query_metric(**kwargs)
    prettify(response)


@output.command("delete-metric")
@cli_args.JOBID_REQUIRED
@cli_args.ROLE_IDE_REQUIRED
@cli_args.PARTYID_REQUIRED
@cli_args.TASK_NAME_REQUIRED
@click.pass_context
def delete_metric(ctx, **kwargs):
    """
    \b
    -description: Delete metric


    \b
    -usage: flow output delete-metric -j xxx -r guest -p 9999 -tn lr_0

    """
    client: FlowClient = ctx.obj["client"]
    response = client.output.delete_metric(**kwargs)
    prettify(response)


@output.command("query-model")
@cli_args.JOBID_REQUIRED
@cli_args.ROLE_IDE_REQUIRED
@cli_args.PARTYID_REQUIRED
@cli_args.TASK_NAME_REQUIRED
@click.pass_context
def query_model(ctx, **kwargs):
    """
    \b
    -description: Query model

    \b
    -usage: flow output query-model -j xxx -r guest -p 9999 -tn lr_0

    """
    client: FlowClient = ctx.obj["client"]
    response = client.output.query_model(**kwargs)
    prettify(response)


@output.command("download-model")
@cli_args.JOBID_REQUIRED
@cli_args.ROLE_IDE_REQUIRED
@cli_args.PARTYID_REQUIRED
@cli_args.TASK_NAME_REQUIRED
@cli_args.PATH_REQUIRED
@click.pass_context
def download_model(ctx, **kwargs):
    """
    \b
    -description: Download model

    \b
    -usage: flow output download-model -j $JOB_ID -r guest -p 9999 -tn lr_0 -o /data/project/xxx
    """
    client: FlowClient = ctx.obj["client"]
    response = client.output.download_model(**kwargs)
    prettify(response)


@output.command("delete-model")
@cli_args.JOBID_REQUIRED
@cli_args.ROLE_IDE_REQUIRED
@cli_args.PARTYID_REQUIRED
@cli_args.TASK_NAME_REQUIRED
@click.pass_context
def delete_model(ctx, **kwargs):
    """
    \b
    -description: Delete Model

    \b
    -usage: flow output delete-model -j $JOB_ID -r guest -p 9999 -tn lr_0

    """
    client: FlowClient = ctx.obj["client"]
    response = client.output.delete_model(**kwargs)
    prettify(response)


@output.command("download-data")
@cli_args.JOBID_REQUIRED
@cli_args.ROLE_IDE_REQUIRED
@cli_args.PARTYID_REQUIRED
@cli_args.TASK_NAME_REQUIRED
@cli_args.PATH_REQUIRED
@click.pass_context
def download_data(ctx, **kwargs):
    """
    \b
    -description: Download Data

    \b
    -usage: flow output download-data -j xxx -r guest -p 9999 -tn lr_0 -o /data/project/xx

    """
    client: FlowClient = ctx.obj["client"]
    response = client.output.download_data(**kwargs)
    prettify(response)


@output.command("query-data-table")
@cli_args.JOBID_REQUIRED
@cli_args.ROLE_IDE_REQUIRED
@cli_args.PARTYID_REQUIRED
@cli_args.TASK_NAME_REQUIRED
@click.pass_context
def table_data(ctx, **kwargs):
    """
    \b
    -description: Query output data table info

    \b
    -usage: flow output query-data-table -j xxx -r guest -p 9999 -tn lr_0

    """
    client: FlowClient = ctx.obj["client"]
    response = client.output.data_table(**kwargs)
    prettify(response)


@output.command("display-data", short_help="Display data")
@cli_args.JOBID_REQUIRED
@cli_args.ROLE_IDE_REQUIRED
@cli_args.PARTYID_REQUIRED
@cli_args.TASK_NAME_REQUIRED
@click.pass_context
def display_data(ctx, **kwargs):
    """
    \b
    -description: Display Data

    \b
    -usage: flow output display-data -j xxx -r guest -p 9999 -tn lr_0

    """
    client: FlowClient = ctx.obj["client"]
    response = client.output.data_display(**kwargs)
    prettify(response)
