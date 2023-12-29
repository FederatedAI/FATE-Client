# FATE Pipeline

FATE Cli is a high-level python API that allows user to design, start,
and query FATE jobs in a sequential manner. FATE Pipeline is designed to
be user-friendly. User can customize job workflow by adding components to pipeline
and then initiate a job with one call. In addition, Pipeline provides
functionality to run prediction and query information after fitting a
pipeline.

## A FATE Job is A Directed Acyclic Graph

A FATE job is a dag that consists of algorithm component nodes. FATE
pipeline provides easy-to-use tools to configure order and setting of
the tasks.

FATE is written in a modular style. Modules are designed to have input
and output data and model. Therefore, two components are connected when
a downsteam component takes output from another component as input. By
tracing how one data set is processed through FATE components, we can see
that a FATE job is in fact formed by a sequence of sub-tasks. For
example, in the [tutorial](https://github.com/FederatedAI/FATE/tree/master/doc/tutorial/pipeline_tutorial_hetero.ipynb),
guest’s and host's data are read in through `DataWarehouseChannel`.
`PSI` then finds overlapping ids between guest and host. Finally, `CoordinatedLR` is fit
on the data. Each listed components run a small task with the data, and
together they constitute a model training job.


## Install Client Cli
``` sourceCode bash
pip install fate-client
```
### FLOW Client CLI

After successfully installed FATE Client, user needs to configure server
information for Client. Client cli provides a command
line tool for quick setup. Run the following command for more
information.

``` sourceCode bash
flow init --help 
```

## Interface of Flow Client 


### Client
Client operational.
[examples] (https://github.com/FederatedAI/FATE-Client/blob/dev-2.0.0-rc/python/fate_client/flow_cli/build/doc/client.md)


### data
Provides numbers of data operational
[examples] (https://github.com/FederatedAI/FATE-Client/blob/dev-2.0.0-rc/python/fate_client/flow_cli/build/doc/data.md)


## job
Provides numbers of job operational commands
[examples] (https://github.com/FederatedAI/FATE-Client/blob/dev-2.0.0-rc/python/fate_client/flow_cli/build/doc/job.md)

## log
Operations related to job logs
[examples] (https://github.com/FederatedAI/FATE-Client/blob/dev-2.0.0-rc/python/fate_client/flow_cli/build/doc/log.md)

## model
Model Operations
[examples] (https://github.com/FederatedAI/FATE-Client/blob/dev-2.0.0-rc/python/fate_client/flow_cli/build/doc/model.md)

## output
Task output Operations
[examples] (https://github.com/FederatedAI/FATE-Client/blob/dev-2.0.0-rc/python/fate_client/flow_cli/build/doc/output.md)

## perission
Permission Operations
[examples] (https://github.com/FederatedAI/FATE-Client/blob/dev-2.0.0-rc/python/fate_client/flow_cli/build/doc/log.md)

## provider
Provider Operations
[examples] (https://github.com/FederatedAI/FATE-Client/blob/dev-2.0.0-rc/python/fate_client/flow_cli/build/doc/perission.md)

## server
Third-party Service Related Operations
[examples] (https://github.com/FederatedAI/FATE-Client/blob/dev-2.0.0-rc/python/fate_client/flow_cli/build/doc/server.md)

## site
Site Operations
[examples] (https://github.com/FederatedAI/FATE-Client/blob/dev-2.0.0-rc/python/fate_client/flow_cli/build/doc/site.md)

## table
Data Table Operations
[examples] (https://github.com/FederatedAI/FATE-Client/blob/dev-2.0.0-rc/python/fate_client/flow_cli/build/doc/table.md)

## task
Provides numbers of task operational
[examples] (https://github.com/FederatedAI/FATE-Client/blob/dev-2.0.0-rc/python/fate_client/flow_cli/build/doc/task.md)

## test
fate test
[examples] (https://github.com/FederatedAI/FATE-Client/blob/dev-2.0.0-rc/python/fate_client/flow_cli/build/doc/test.md)







