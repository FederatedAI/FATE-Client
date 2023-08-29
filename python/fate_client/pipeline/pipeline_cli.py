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

from pathlib import Path

import click
from ruamel import yaml

default_config = Path(__file__).parent.parent.joinpath("settings.yaml").resolve()


@click.group(name="pipeline")
def pipeline_group():
    ...


@pipeline_group.command(name="init", help="pipeline init")
@click.option("--ip", type=click.STRING, help="Fate Flow server ip address.")
@click.option("--port", type=click.INT, help="Fate Flow server port.")
@click.option("--path", type=click.STRING, help="config pipeline by file directly")
def _init_pipeline(**kwargs):
    """
    pipeline config
    """
    ip = kwargs.get("ip")
    port = kwargs.get("port")
    path = kwargs.get("path")

    config_path = default_config

    with Path(config_path).open("r") as fin:
        config = yaml.safe_load(fin)

    flow_config = dict()
    if ip:
        flow_config["ip"] = ip
    if port:
        flow_config["port"] = port

    if flow_config:
        config["flow_service"].update(flow_config)
    elif path:
        with Path(path).open("r") as fin:
            config = yaml.safe_load(fin)

    with default_config.open("w") as fout:
        yaml.dump(config, fout, Dumper=yaml.RoundTripDumper)

    print("Pipeline configuration succeeded.")


@pipeline_group.command(name="site-info", help="pipeline site info")
@click.option("--role", type=click.STRING, help="local role")
@click.option("--party", type=click.STRING, help="local party id.")
def _init_pipeline(**kwargs):
    """
    pipeline config
    """
    role = kwargs.get("role")
    party = kwargs.get("party")

    config_path = default_config

    with Path(config_path).open("r") as fin:
        config = yaml.safe_load(fin)

    site_info_config = dict()
    if role:
        site_info_config["local_role"] = role
    if party:
        site_info_config["local_party_id"] = party

    if site_info_config:
        config["pipeline"]["site_info"].update(site_info_config)

    with default_config.open("w") as fout:
        yaml.dump(config, fout, Dumper=yaml.RoundTripDumper)

    print("Pipeline site info configuration succeeded.")


@pipeline_group.command(name="show")
def _show():
    """
        \b
        - DESCRIPTION:
            Show pipeline config details for Flow server.
        \b
        - USAGE:
            pipeline config show
    """
    with Path(default_config).open("r") as fin:
        config = yaml.safe_load(fin)
        click.echo(f"\nPipeline Config: {yaml.dump(config)}")


