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
from ..utils.cli_utils import load_yaml, prettify
from fate_client.flow_sdk import FlowClient


@click.group()
@click.pass_context
def job(ctx):
    """
    \b
    -description: Provides numbers of job operational commands, including submit, stop, query etc. For more details, please check out the help text.
    """
    pass


@job.command("submit")
@cli_args.CONF_PATH
@click.pass_context
def submit(ctx, **kwargs):
    """
    \b
    -description: Submit and create a job.

    \b
    -usage: flow job submit -c examples/lr/train_lr.yaml
    """
    dag_schema = load_yaml(kwargs.get("conf_path"))
    client: FlowClient = ctx.obj["client"]
    response = client.job.submit(dag_schema=dag_schema)
    prettify(response)


@job.command("query")
@cli_args.JOBID
@cli_args.ROLE_IDE
@cli_args.PARTYID
@cli_args.STATUS
@click.pass_context
def query(ctx, **kwargs):
    """
    \b
    -description: Querying jobs through filtering conditions.

    \b
    -usage: flow job query -j 202308211557455662860 -r guest -p 9999 -s running
    """
    client: FlowClient = ctx.obj["client"]
    response = client.job.query(**kwargs)
    prettify(response)


@job.command("add-notes")
@cli_args.JOBID_REQUIRED
@cli_args.ROLE_IDE_REQUIRED
@cli_args.PARTYID_REQUIRED
@cli_args.NOTES_REQUIRED
@click.pass_context
def add_notes(ctx, **kwargs):
    """
    \b
    -description: Add notes for job.

    \b
    -usage: flow job add-notes -j 202308211557455662860 -r guest -p 9999 --notes "this is a test"
    """
    client: FlowClient = ctx.obj["client"]
    response = client.job.add_notes(**kwargs)
    prettify(response)


@job.command("stop")
@cli_args.JOBID_REQUIRED
@click.pass_context
def stop(ctx, **kwargs):
    """
    \b
    -description: Stopping a running job.

    \b
    -usage: flow job stop -j 202308211557455662860
    """
    client: FlowClient = ctx.obj["client"]
    response = client.job.stop(**kwargs)
    prettify(response)


@job.command("rerun")
@cli_args.JOBID_REQUIRED
@click.pass_context
def rerun(ctx, **kwargs):
    """
    \b
    -description: Rerunning a failed job.

    \b
    -usage: flow job rerun -j 202308211557455662860
    """
    client: FlowClient = ctx.obj["client"]
    response = client.job.rerun(**kwargs)
    prettify(response)


@job.command("list")
@cli_args.JOBID
@cli_args.ROLE_IDE
@cli_args.PARTYID
@cli_args.STATUS
@cli_args.LIMIT
@click.pass_context
def job_list(ctx, **kwargs):
    """
    \b
    -description: Fetching a list of jobs based on conditions.

    \b
    -usage: flow job list -j 202308211557455662860 -r guest -p 9999
    """
    client: FlowClient = ctx.obj["client"]
    response = client.job.query_job_list(**kwargs)
    prettify(response)


@job.command("download-log")
@cli_args.JOBID_REQUIRED
@cli_args.PATH_REQUIRED
@click.pass_context
def log(ctx, **kwargs):
    """
    \b
    -description: Downloading job logs.

    \b
    -usage: flow job download-log -j 202308211557455662860 -o /data/project/examples/
    """
    client: FlowClient = ctx.obj["client"]
    response = client.job.download_log(**kwargs)
    prettify(response)


@job.command("clean-queue")
@click.pass_context
def clean_queue(ctx):
    """
    \b
    -description： Cleaning up the queued job queue.

    \b
    -usage: flow job clean-queue
    """
    client: FlowClient = ctx.obj["client"]
    response = client.job.queue_clean()
    prettify(response)


@job.command("clean")
@cli_args.JOBID_REQUIRED
@click.pass_context
def clean(ctx, **kwargs):
    """
    \b
    -description: Cleaning up job output data.

    \b
    -usage: flow job clean -j 202308211557455662860
    """
    client: FlowClient = ctx.obj["client"]
    response = client.job.job_clean(**kwargs)
    prettify(response)


@job.command("dependency")
@cli_args.JOBID_REQUIRED
@cli_args.ROLE_IDE_REQUIRED
@cli_args.PARTYID_REQUIRED
@click.pass_context
def dependency(ctx, **kwargs):
    """
    -description: Dependency relationships between tasks within a job.

    \b
    -usage: flow job dependency -j 202308211557455662860 -r guest -p 9999

    """
    client: FlowClient = ctx.obj["client"]
    response = client.job.dag_dependency(**kwargs)
    prettify(response)
