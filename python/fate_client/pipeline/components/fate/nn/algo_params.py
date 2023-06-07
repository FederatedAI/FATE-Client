from transformers import TrainingArguments as _hf_TrainingArguments
from dataclasses import dataclass, field, fields
from enum import Enum


@dataclass
class TrainingArguments(_hf_TrainingArguments):
    
    # By default, we disable tqdm progress bar for logging conerns.
    output_dir: str = field(default="./")
    disable_tqdm: bool = field(default=True)
    save_strategy: str = field(default="no")
    logging_strategy: str = field(default="epoch")
    evaluation_strategy: str = field(default="no")



class AggregateStrategy(Enum):
    EPOCH = "epoch"
    STEP = "step"


@dataclass
class FedArguments(object):
    """
    The argument for Fed algorithm
    """
    aggregate_strategy: AggregateStrategy = field(default=AggregateStrategy.EPOCH.value)
    aggregate_freq: int = field(default=1)

    def to_dict(self):
        """
        Serializes this instance while replace `Enum` by their values (for JSON serialization support). It obfuscates
        the token values by removing their value.
        """
        # filter out fields that are defined as field(init=False)
        d = dict((field.name, getattr(self, field.name)) for field in fields(self) if field.init)

        for k, v in d.items():
            if isinstance(v, Enum):
                d[k] = v.value
            if isinstance(v, list) and len(v) > 0 and isinstance(v[0], Enum):
                d[k] = [x.value for x in v]
            if k.endswith("_token"):
                d[k] = f"<{k.upper()}>"
        return d
    

@dataclass
class FedAVGArguments(FedArguments):

    """
    The arguemnt for FedAVG algorithm, used in FedAVGClient and FedAVGServer.

    Attributes:
        weighted_aggregate: bool
            Whether to use weighted aggregation or not.
        secure_aggregate: bool
            Whether to use secure aggregation or not.
    """
        
    weighted_aggregate: bool = field(default=True)
    secure_aggregate: bool = field(default=False)