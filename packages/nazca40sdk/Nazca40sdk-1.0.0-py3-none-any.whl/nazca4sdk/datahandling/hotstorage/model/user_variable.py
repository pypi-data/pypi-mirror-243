import re
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from typing import Optional


class UserVariableDataType(Enum):
    BOOL = 0
    INT = 1
    DOUBLE = 2
    TEXT = 3
    DATETIME = 4


@dataclass()
class UserVariable:
    type: UserVariableDataType
    name: str
    value: object
    datetime: Optional[datetime] = None

    def __post_init__(self):
        if self.datetime is None:
            self.datetime = datetime.now()
        if self.type == UserVariableDataType.DATETIME and isinstance(self.value, str):
            if re.search("[+-][0-9][0-9]:[0-9][0-9]", self.value):
                raise ValueError("DataTime value can't contain time offset")


@dataclass()
class UserVariableInfo:
    type: UserVariableDataType
    name: str
