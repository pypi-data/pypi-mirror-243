from dataclasses import dataclass


@dataclass
class Prediction:
    topic: str
    topic_group: str
    executor: str
