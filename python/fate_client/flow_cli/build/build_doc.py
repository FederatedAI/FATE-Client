import os.path
import re

import click
from click.core import Group

from fate_client.flow_cli.flow import flow_cli

comm = "flow"

types = ["TEXT", "INTEGER", "PATH"]

BASE_DIR = "./doc"
USAGE_PATTERN = r"-(.*)usage:\s+(.*)"
DESCRIPTION_PATTERN = r"-(.*)description:\s+(.*)"
PARAMS_PATTERN = r"Options:(.*?)(?=\s*--help)"


def get_description(help_str):
    match = re.search(DESCRIPTION_PATTERN, help_str)
    desc = ""
    if match:
        desc = match.group(2)
    return desc


def get_usage(help_str):
    match = re.search(USAGE_PATTERN, help_str)
    usage = ""
    if match:
        usage = match.group(2)
    return usage


def get_params(help_str):
    pattern = re.compile(PARAMS_PATTERN, re.DOTALL)
    match = pattern.search(help_str)
    params_list = []
    if match:
        desc = match.group(1)
        lines = desc.strip().split('\n')
        for line in lines:
            required, type, desc, command_params = parse_param(line)
            if required and not type and not desc and not command_params:
                params_list[-1] = ('yes', params_list[-1][1], params_list[-1][2], params_list[-1][3])
                continue
            if required or type or desc or command_params:
                params_list.append((required, type, desc, command_params))
    return params_list


def parse_param(param_str):
    required = None
    try:
        params = param_str.split(",")
        required = is_required(params)
        if params:
            type, desc, command_params = params_type_desc(params)
            return required, type, desc, command_params
    except:
        if required == "yes":
            return required, None, None, None
        else:
            return None, None, None, None


def is_required(lines):
    if "[required]" in lines[-1]:
        lines[-1] = lines[-1].strip("[required]")
        return "yes"
    return "no"


def params_type_desc(lines):
    line = lines[-1]
    for _type in types:
        if _type in line:
            _item = line.split(_type)
            _desc = _item[-1].strip()
            command_params = lines[:-1] + [_item[0].strip()]
            if _type == "TEXT":
                _type = "STR"
            return _type.lower(), _desc, command_params


def write_command(f, group_commands, group_cli):
    commands = group_commands
    if isinstance(group_commands, dict):
        commands = group_commands.values()
    for cli in commands:
        with click.Context(cli) as ctx:
            _cli_comm = group_cli + " " + cli.name + " [OPTIONS]"
            _h = cli.get_help(ctx)
            desc = get_description(_h)
            usage = get_usage(_h)
            params_list = get_params(_h)
            f.write(f"### {cli.name}\n")
            f.write(desc + "\n")
            f.write(f"```bash\n{_cli_comm}\n```\n")
            write_options(f, params_list)
            write_usage(f, usage)


def write_options(f, params_list):
    if params_list and len(params_list):
        f.write(f"**Options**\n")
        f.write("\n| parameters | short-format | long-format | required | type | description |\n")
        f.write("| :-------- |:-----|:-------------| :--- | :----- |------|\n")
        # for params in params_list:
        for params in params_list:
            params_format = params[-1]
            if not params_format:
                continue
            if len(params_format) == 2:
                short_format = params_format[0].strip()
                long_format = params_format[1].strip()
            elif len(params_format) == 1:
                short_format = ""
                long_format = ""

                if "--" in params_format[0]:
                    long_format = params_format[0].strip()

                else:
                    short_format = params_format[0].strip()

            else:
                raise ValueError(params_format)

            parameters = long_format.lstrip('-').replace('-', '_')
            short_format = f"`{short_format}`" if short_format else "-"
            f.write(f"| {parameters} | {short_format} | `{long_format}` | {params[0]} | {params[1]} | {params[2]} |\n")


def write_usage(f, usage):
    f.write(f"\n**Usage**\n")
    f.write(f"```bash\n{usage}\n```\n\n")


def write_init(init_list):
    _doc_file = os.path.join(BASE_DIR, f"flow.md")
    with open(_doc_file, "w") as f:
        f.write(f"## flow\n")
        f.write("FATE Flow client\n")
        write_command(f, init_list, comm)


def make_markdown():
    _init_comm_list = []
    os.makedirs(BASE_DIR, exist_ok=True)
    for i in [cmd for cmd in flow_cli.commands]:
        group = flow_cli.get_command(click.pass_context, i)
        _comm = comm
        if isinstance(group, Group):
            group_title = group.help.strip()
            _doc_file = os.path.join(BASE_DIR, f"{group.name}.md")
            with open(_doc_file, "w") as f:
                f.write(f"## {group.name}\n")
                if group_title:
                    f.write(get_description(group_title) + "\n")
                group_cli = comm + " " + group.name
                group_commands = group.commands
                write_command(f, group_commands, group_cli)
        else:
            _init_comm_list.append(group)

    write_init(_init_comm_list)


make_markdown()
