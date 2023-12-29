# FATE CLIENT 

Description

Introduces how to install and use the FATE Flow Client, which is usually
included in the FATE Client, which contains several clients of the FATE 
Project: Pipeline, FATE Flow Client and FATE Test.

Introducing the command line provided by FATE Flow Client, all commands will
have a common invocation entry, you can type flow in the command line to get all
the command categories and their subcommands.

    [IN]
    flow

    [OUT]
    Usage: flow [OPTIONS] COMMAND [ARGS]...

      Fate Flow Client

    Options.
      -h, --help Show this message and exit.

    Commands: -h, --help
      client      -description: Client Operations
      data        -description: Provides numbers of data operational...
      init        -description: Flow CLI Init Command.
      job         -description: Provides numbers of job operational commands,...
      log         -description: Operations related to job logs.
      model       -description: Model Operations
      output      -description: Task output Operations
      permission  -description: Permission Operations
      provider    -description: Provider Operations
      server      -description: Third-party Service Related Operations
      site        -description: Site Operations
      table       -description: Data Table Operations, such as Querying and...
      task        -description: Provides numbers of task operational...
      test        -description: fate test
      version     -description: Get fate flow client version -usage: flow...


## Install FATE Client
FATE Client will be distributed to pypi, you can install the corresponding version directly
using tools such as pip, e.g.

    pip install fate-client

## INIT FATE Client

    flow init   -h 
    Usage: flow init [OPTIONS]

    -description: Flow CLI Init Command. provide ip and port of a valid fate flow server.
    If the server enables client authentication, you need to configure app-id and app-token
      
    -usage: flow init --ip 127.0.0.1 --port 9380
    
    Options:
      --ip TEXT         Fate flow server ip address.
      --port INTEGER    Fate flow server port.
      --app-id TEXT     APP key for sign requests.
      --app-token TEXT  Secret key for sign requests.
      --reset           If specified, initialization settings would be reset to
                        none. Users should init flow again.
      -h, --help        Show this message and exit.


### FLOW Client CLI

After successfully installed FATE Client,and init FATE Client. user needs to configure server
information for Client. Client cli provides a command
line tool for quick setup. Run the following command for more
information.


## Interface of Flow Client 

### Client
Client operational.
[examples] (https://github.com/FederatedAI/FATE-Client/blob/master/python/fate_client/flow_cli/build/doc/client.md)


### data
Provides numbers of data operational
[examples] (https://github.com/FederatedAI/FATE-Client/blob/master/python/fate_client/flow_cli/build/doc/data.md)


## job
Provides numbers of job operational commands
[examples] (https://github.com/FederatedAI/FATE-Client/blob/master/python/fate_client/flow_cli/build/doc/job.md)

## log
Operations related to job logs
[examples] (https://github.com/FederatedAI/FATE-Client/blob/master/python/fate_client/flow_cli/build/doc/log.md)

## model
Model Operations
[examples] (https://github.com/FederatedAI/FATE-Client/blob/master/python/fate_client/flow_cli/build/doc/model.md)

## output
Task output Operations
[examples] (https://github.com/FederatedAI/FATE-Client/blob/master/python/fate_client/flow_cli/build/doc/output.md)

## perission
Permission Operations
[examples] (https://github.com/FederatedAI/FATE-Client/blob/master/python/fate_client/flow_cli/build/doc/log.md)

## provider
Provider Operations
[examples] (https://github.com/FederatedAI/FATE-Client/blob/master/python/fate_client/flow_cli/build/doc/perission.md)

## server
Third-party Service Related Operations
[examples] (https://github.com/FederatedAI/FATE-Client/blob/master/python/fate_client/flow_cli/build/doc/server.md)

## site
Site Operations
[examples] (https://github.com/FederatedAI/FATE-Client/blob/master/python/fate_client/flow_cli/build/doc/site.md)

## table
Data Table Operations
[examples] (https://github.com/FederatedAI/FATE-Client/blob/master/python/fate_client/flow_cli/build/doc/table.md)

## task
Provides numbers of task operational
[examples] (https://github.com/FederatedAI/FATE-Client/blob/master/python/fate_client/flow_cli/build/doc/task.md)

## test
fate test
[examples] (https://github.com/FederatedAI/FATE-Client/blob/master/python/fate_client/flow_cli/build/doc/test.md)







