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
import os
import time
import click
from fate_client.flow_cli.utils import cli_args
from fate_client.flow_cli.utils.cli_utils import prettify
from fate_client.flow_sdk import FlowClient


@click.group()
@click.pass_context
def test(ctx):
    """
    \b
    -description: fate test

    """
    pass


@test.command("toy")
@cli_args.GUEST_PARTYID_REQUIRED
@cli_args.HOST_PARTYID_REQUIRED
@cli_args.TIMEOUT
# @cli_args.TASK_CORES
@click.pass_context
def toy(ctx, **kwargs):
    """
    \b
    -description: Connectivity test.

    \b
    -usage: flow test toy -gid 9999 -hid 10000
    """
    flow_sdk = FlowClient(ip=ctx.obj["ip"], port=ctx.obj["http_port"], version=ctx.obj["api_version"],
                          app_id=ctx.obj.get("app_id"), app_token=ctx.obj.get("app_token"))
    submit_result = flow_sdk.test.toy(**kwargs)
    if submit_result["code"] == 0:
        job_id = submit_result["job_id"]
        for t in range(kwargs["timeout"]):
            party_id = kwargs["guest_party_id"]
            info = flow_sdk.site.info()
            if info.get("code") == 0:
                party_id = info.get("data", {}).get("party_id", kwargs["guest_party_id"])
            r = flow_sdk.job.query(job_id=job_id, party_id=party_id)
            if r["code"] == 0 and len(r["data"]):
                job_status = r["data"][0]["status"]
                print(f"toy test job {job_id} is {job_status}")
                if job_status in {"failed", "canceled"}:
                    warn_print(job_id)
                    break
                if job_status in {"success"}:
                    break
            time.sleep(1)
        else:
            print(f"timeout...")
            warn_print(job_id)
            try:
                flow_sdk.job.stop(job_id=job_id)
            except:
                pass
    else:
        prettify(submit_result)


def warn_print(job_id):
    print(f"You can use the command of 'flow job download-log -j {job_id} -o $download_dir' to download the logs.")
