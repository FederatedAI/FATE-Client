## Release 2.1.1
### Major improvements
* Pipeline: add dump and load interface
* Pipeline: Support FATE-LLM 2.1.0, add FedMKT support

## Release 2.1.0
### Major improvements
* Pipeline: add supports for fate-llm 2.0
  * newly added LLMModelLoader, LLMDatasetLoader, LLMDataFuncLoader
  * newly added configuration parsing of seq2seq_runner and ot_runner
* Pipeline: unified input interface of components

## Release 2.0.0
### Feature Highlights
> FATE-Client 2.0: Building Scalable Federated DSL for Application Layer Interconnection
* Introduce new scalable and standardized federated DSL IR(Intermediate Representation) for federated modeling job
* Compile python client to DSL IR
* Federated DSL IR extension enhancement: supports multi-party asymmetric scheduling
* Support mutual translation between Standardized Fate-2.0.0 DSL IR and BFIA protocol
* Support using components with BFIA protocol through adapter mode
* Migrated Flow CLI and Flow SDK
