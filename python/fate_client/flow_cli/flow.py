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
from ruamel import yaml
from pathlib import Path
from fate_client.flow_sdk import FlowClient
from fate_client.flow_cli.commands import client, job, data, log, model, output, permission, provider, server, site, table, task, test
from fate_client.flow_cli.utils.cli_utils import prettify, connect_service


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

config_path = Path(__file__).parent.parent.joinpath("settings.yaml").resolve()


@click.group(short_help='Fate Flow Client', context_settings=CONTEXT_SETTINGS)
@click.pass_context
def flow_cli(ctx):
    '''
    Fate Flow Client
    '''
    ctx.ensure_object(dict)
    if ctx.invoked_subcommand == 'init':
        return

    with open(config_path, 'r') as fin:
        config = yaml.safe_load(fin)
        flow_config = config['flow_service']
    if not flow_config.get('api_version'):
        raise ValueError('api_version in config is required')
    ctx.obj['api_version'] = flow_config['api_version']

    if flow_config.get('ip') and flow_config.get('port'):
        ctx.obj['ip'] = flow_config['ip']
        ctx.obj['http_port'] = int(flow_config['port'])
        ctx.obj['server_url'] = f'http://{ctx.obj["ip"]}:{ctx.obj["http_port"]}/{flow_config["api_version"]}'
        if flow_config.get('app_id') and flow_config.get('app_token'):
            ctx.obj['app_id'] = flow_config['app_id']
            ctx.obj['app_token'] = flow_config['app_token']
    else:
        raise ValueError('Invalid configuration file. Did you run "flow init"?')

    ctx.obj['initialized'] = (flow_config.get('ip') and flow_config.get('port'))
    if ctx.obj['initialized']:
        ctx.obj["client"] = FlowClient(
            ip=flow_config.get('ip'), port=flow_config.get('port'), version=flow_config.get("api_version"),
            app_id=flow_config.get("app_id"), app_token=flow_config.get('app_token')
        )


@flow_cli.command('init')
@click.option('--ip', type=click.STRING, help='Fate flow server ip address.')
@click.option('--port', type=click.INT, help='Fate flow server port.')
@click.option('--app-id', type=click.STRING, help='APP key for sign requests.')
@click.option('--app-token', type=click.STRING, help='Secret key for sign requests.')
@click.option('--reset', is_flag=True, default=False,
              help='If specified, initialization settings would be reset to none. Users should init flow again.')
def initialization(**kwargs):
    """
    \b
    -description: Flow CLI Init Command. provide ip and port of a valid fate flow server.If the server enables client authentication, you need to configure app-id and app-token
    \b
    -usage: flow init --ip 127.0.0.1 --port 9380
    """

    with open(config_path, 'r') as fin:
        config = yaml.safe_load(fin)
        flow_config = config['flow_service']

    if kwargs.get('reset'):
        flow_config['api_version'] = 'v2'
        for i in ('ip', 'port', 'app_id', 'app_token'):
            flow_config[i] = None

        with open(config_path, 'w') as fout:
            yaml.dump(flow_config, fout, Dumper=yaml.RoundTripDumper)
        prettify(
            {
                'code': 0,
                'retmsg': 'Fate Flow CLI has been reset successfully. '
                          'Please do initialization again before you using flow CLI v2.'
            }
        )
    else:
        flow_config['api_version'] = 'v2'
        _update = False
        for i in ('ip', 'port', 'app_id', 'app_token'):
            if kwargs.get(i):
                flow_config[i] = kwargs[i]
                _update = True

        if not connect_service(flow_config["ip"], flow_config["port"]):
            prettify(
                {
                    'code': 100,
                    'retmsg': 'Fate Flow CLI initialization failed：Unable to connect to the server, Please check if the IP or port is correct.'
                }
            )
            return

        if _update:
            with open(config_path, 'w') as fout:
                yaml.dump(config, fout, Dumper=yaml.RoundTripDumper)
            prettify(
                {
                    'code': 0,
                    'retmsg': 'Fate Flow CLI has been initialized successfully.'
                }
            )
        else:
            prettify(
                {
                    'code': 100,
                    'retmsg': 'Fate Flow CLI initialization failed.'
                }
            )


@flow_cli.command('version')
def get_version():
    """
    \b
    -description: Get fate flow client version
    \b
    -usage: flow version

    """
    import fate_client
    print(fate_client.__version__)


flow_cli.add_command(client.client)
flow_cli.add_command(job.job)
flow_cli.add_command(data.data)
flow_cli.add_command(log.log)
flow_cli.add_command(model.model)
flow_cli.add_command(output.output)
flow_cli.add_command(permission.permission)
flow_cli.add_command(provider.provider)
flow_cli.add_command(server.server)
flow_cli.add_command(site.site)
flow_cli.add_command(table.table)
flow_cli.add_command(task.task)
flow_cli.add_command(test.test)


if __name__ == '__main__':
    flow_cli()
