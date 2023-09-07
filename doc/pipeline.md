# FATE Pipeline

Pipeline is a high-level python API that allows user to design, start,
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

Beyond the given tutorial, a job may include multiple data sets and
models. For more pipeline job examples, please refer to
[examples](https://github.com/FederatedAI/FATE/tree/master/examples/pipeline).

## Install Pipeline

### Pipeline CLI

After successfully installed FATE Client, user needs to configure server
information for Pipeline. Pipeline provides a command
line tool for quick setup. Run the following command for more
information.

``` sourceCode bash
pipeline init --help
```

## Interface of Pipeline

### Component

FATE components are wrapped into `component` in Pipeline API.
When defining a component, user need to specify components' name,
input data(may be named as `input_data` or `train_data`), parameters and, possibly, input model(s).
Each component can take in and output `Data` and `Model`.
Some may take multiple copies of `Data` or `Model`. Parameters of
components can be set conveniently at the time of initialization.
Unspecified parameters will take default values. All components have a
`name`, which can be arbitrarily set. A component’s name is its
identifier, and so it must be unique within a pipeline. We suggest that
each component name includes a numbering as suffix for easy tracking.

An example of initializing a component:

```python
from fate_client.pipeline.components.fate import CoordinatedLR, PSI

lr_0 = CoordinatedLR("lr_0",
                     epochs=10,
                     batch_size=300,
                     optimizer={"method": "SGD", "optimizer_params": {"lr": 0.1}, "penalty": "l2", "alpha": 0.001},
                     init_param={"fit_intercept": True, "method": "zeros"},
                     learning_rate_scheduler={"method": "linear", "scheduler_params": {"start_factor": 0.7,
                                                                                       "total_iters": 100}},
                     train_data=psi_0.outputs["output_data"])

```

### Data

A component may take in or output multiple data input(s).

As a general guideline,
all training components(i.e. model that outputs reusable model) takes in `train_data`, `validate_data`, `test_data`,
and `cv_data`, while
feature engineering, statistical components takes in `input_data`. An exception is `Union` component,
which takes in multiple input data.

For output, training components that can take in `train_data`, `validate_data`, `test_data`, and `cv_data`, generally
may output corresponding output data. Feature engineering, statistical components usually only has `output_data`,
except for `DataSplit` component, which has `train_output_data`, `validate_output_data`, `test_output_data`.

Below lists data input and output of all components:

| Algorithm                | Component Name         | Data Input                                    | Data Output                                                                |
|--------------------------|------------------------|-----------------------------------------------|----------------------------------------------------------------------------|
| PSI                      | PSI                    | input_data                                    | output_data                                                                |
| Sampling                 | Sample                 | input_data                                    | output_data                                                                |
| Data Split               | DataSplit              | input_data                                    | train_output_data, validate_output_data, test_output_data                  |
| Feature Scale            | FeatureScale           | train_data, test_data                         | train_output_data, test_output_data                                        |
| Data Statistics          | Statistics             | input_data                                    | output_data                                                                |
| Hetero Feature Binning   | HeteroFeatureBinning   | train_data, test_data                         | train_output_data, test_output_data                                        |
| Hetero Feature Selection | HeteroFeatureSelection | train_data, test_data                         | train_output_data, test_output_data                                        |
| Coordinated-LR           | CoordinatedLR          | train_data, validate_data, test_data, cv_data | train_output_data, validate_output_data, test_output_data, cv_output_datas |
| Coordinated-LinR         | CoordinatedLinR        | train_data, validate_data, test_data, cv_data | train_output_data, validate_output_data, test_output_data, cv_output_datas |
| Homo-LR                  | HomoLR                 | train_data, validate_data, test_data, cv_data | train_output_data, validate_output_data, test_output_data, cv_output_datas |
| Homo-NN                  | HomoNN                 | train_data, validate_data, test_data, cv_data | train_output_data, validate_output_data, test_output_data, cv_output_datas |
| Hetero Secure Boosting   | HeteroSecureBoost      | train_data, validate_data, test_data, cv_data | train_output_data, validate_output_data, test_output_data, cv_output_datas |
| Evaluation               | Evaluation             | input_data                                    |                                                                            |
| Union                    | Union                  | input_data_list                               | output_data                                                                |

### Model

`Model` defines model input and output of components. Similar to `Data`,
components may take in single or multiple input models. All components can either has one or no model output.
Model training components also may take `warm_start_model`, but note that only one of the two models should be provided.

Below lists model input and output of all components:

| Algorithm                | Component Name         | Model Input                   | Model Output |
|--------------------------|------------------------|-------------------------------|--------------|
| PSI                      | PSI                    |                               |              |
| Sampling                 | Sample                 |                               |              |
| Data Split               | DataSplit              |                               |              |
| Feature Scale            | FeatureScale           | input_model                   | output_model |
| Data Statistics          | Statistics             |                               | output_model |
| Hetero Feature Binning   | HeteroFeatureBinning   | input_model                   | output_model |
| Hetero Feature Selection | HeteroFeatureSelection | input_models, input_model     | output_model |
| Coordinated-LR           | CoordinatedLR          | input_model, warm_start_model | output_model |
| Coordinated-LinR         | CoordinatedLinR        | input_model, warm_start_model | output_model |
| Homo-LR                  | HomoLR                 | input_model, warm_start_model | output_model |
| Homo-NN                  | HomoNN                 | input_model, warm_start_model | output_model |
| Hetero Secure Boosting   | HeteroSecureBoost      | input_model, warm_start_model | output_model |
| Evaluation               | Evaluation             |                               |              |
| Union                    | Union                  |                               |              |

## Build A Pipeline

Below is a general guide to building a pipeline.

Once initialized a pipeline, job participants and initiator should be
specified. Below is an example of initial setup of a pipeline:

```python
from fate_client.pipeline import FateFlowPipeline

pipeline = FateFlowPipeline().set_roles(guest='9999', host='10000', arbiter='10000')
```

User may also specify runtime configuration:

```python
pipeline.conf.set("task_cores", 4)
pipeline.conf.set("timeout", 3600)
```

All pipeline components can be configured individually for different
roles. For instance, `PSI`
component can be configured specifically for each party like this:

```python
psi_0 = PSI("psi_0")
psi_0.guest.component_setting(input_data=DataWarehouseChannel(name="breast_hetero_guest",
                                                              namespace="experiment"))
psi_0.hosts[0].component_setting(input_data=DataWarehouseChannel(name="breast_hetero_host",
                                                                 namespace="experiment"))
```

To include a component in a pipeline, use `add_task`. To add the
`PSI` component to the previously created pipeline, try
this:

```python
pipeline.add_task(psi_0)
```

## Run A Pipeline

Having added all components, user needs to first compile pipeline before
running the designed job. After compilation, the pipeline can then be
fit(run train job).

```python
pipeline.compile()
pipeline.fit()
```

## Query on Tasks

FATE Pipeline provides API to query component information, including
output data, model, and metrics.

```python
output_model = pipeline.get_task_info("lr_0").get_output_model()
```

## Deploy Components

Once fitting pipeline completes, prediction can be run on new data set.
Before prediction, necessary components need to be first deployed. This
step marks selected components to be used by prediction pipeline.

```python
# deploy select components
pipeline.deploy([psi_0, lr_0])
```

## Predict with Pipeline

First, initiate a new pipeline, then specify data source used for
prediction.

```python
predict_pipeline = FateFlowPipeline()

deployed_pipeline = pipeline.get_deployed_pipeline()
deployed_pipeline.psi_0.guest.component_setting(
    input_data=DataWarehouseChannel(name="breast_hetero_guest",
                                    namespace=f"experiment{namespace}"))
deployed_pipeline.psi_0.hosts[0].component_setting(
    input_data=DataWarehouseChannel(name="breast_hetero_host",
                                    namespace=f"experiment{namespace}"))

predict_pipeline.add_task(deployed_pipeline)
predict_pipeline.compile()
```

New pipeline can then initiate prediction.

```python
    predict_pipeline.predict()
```

## Local File to DataFrame

PipeLine provides functionality to transform local data table into FATE DataFrame. Please refer
to
this [demo](https://github.com/FederatedAI/FATE/tree/master/doc/tutorial/pipeline_tutorial_transform_local_file_to_dataframe.ipynb)
for a quick example.
