import json
from typing import Union
from enum import Enum
from dataclasses import dataclass


class EventType(Enum):
    DIAL_EVENT = 0
    HANDSET_EVENT = 1


class HandsetState(Enum):
    HUNG_UP = 0
    PICKED_UP = 1


@dataclass(frozen=True)
class DialEvent:
    type: EventType
    data: Union[HandsetState, int]

    def __repr__(self):
        j = {"type": self.type.value}
        if isinstance(self.data, int):
            j["data"] = self.data
        else:
            j["data"] = self.data.value
        return json.dumps(j)

    def __str__(self):
        return f"DIAL EVENT\n\ttype: {self.type}\n\tdata: {self.data}"
