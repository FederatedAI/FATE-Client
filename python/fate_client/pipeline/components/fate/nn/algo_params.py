from transformers import TrainingArguments as _hf_TrainingArguments
from dataclasses import dataclass, field, fields
from enum import Enum


class AggregateStrategy(Enum):
    EPOCH = "epochs"
    STEP = "steps"


class AggregatorType(Enum):
    PLAINTEXT = "plaintext"
    SECURE_AGGREGATE = "secure_aggregate"


@dataclass
class FedArguments(object):
    """
    The argument for Fed algorithm
    """

    aggregate_strategy: AggregateStrategy = field(default=AggregateStrategy.EPOCH.value)
    aggregate_freq: int = field(default=1)
    aggregator: str = field(default=AggregatorType.SECURE_AGGREGATE.value)

    def to_dict(self):
        """
        Serializes this instance while replace `Enum` by their values (for JSON serialization support). It obfuscates
        the token values by removing their value.
        """
        # filter out fields that are defined as field(init=False)
        d = dict(
            (field.name, getattr(self, field.name))
            for field in fields(self)
            if field.init
        )

        for k, v in d.items():
            if isinstance(v, Enum):
                d[k] = v.value
            if isinstance(v, list) and len(v) > 0 and isinstance(v[0], Enum):
                d[k] = [x.value for x in v]
            if k.endswith("_token"):
                d[k] = f"<{k.upper()}>"
        return d


@dataclass
class TrainingArguments(_hf_TrainingArguments):
    # in fate-2.0, we will control the output dir when using pipeline
    output_dir: str = field(default="./")
    disable_tqdm: bool = field(default=True)
    save_strategy: str = field(default="no")
    logging_strategy: str = field(default="epoch")
    evaluation_strategy: str = field(default="no")
    logging_dir: str = field(default=None)
    checkpoint_idx: int = field(default=None)
    # by default we use constant learning rate, the same as FATE-1.X
    lr_scheduler_type: str = field(default="constant")

    def __post_init__(self):
        # Always use default values for hub-related attributes
        self.push_to_hub = False
        self.hub_model_id = None
        self.hub_strategy = "every_save"
        self.hub_token = None
        self.hub_private_repo = False
        self.push_to_hub_model_id = None
        self.push_to_hub_organization = None
        self.push_to_hub_token = None

        super().__post_init__()

    def to_dict(self):
        # Call the superclass's to_dict method
        # print(self.logging_dir)
        all_args = super().to_dict()

        # Get a dict with default values for all fields
        default_args = _hf_TrainingArguments(output_dir="./").to_dict()

        # Filter out args that are equal to their default values
        set_args = {
            name: value
            for name, value in all_args.items()
            if value != default_args.get(name)
        }

        return set_args


@dataclass
class FedAVGArguments(FedArguments):
    pass
