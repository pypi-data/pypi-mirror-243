from enum import Enum


class KnowledgeDataType(str, Enum):
    TEXT = "text"
    NUM = "num"
    FORMAT = "format"
    IMAGE = "img"
    BLOB = "blob"
    LINK = "link"
    BOOL = "bool"
    CHART = "chart"

    @classmethod
    def has_value(cls, value):
        if not isinstance(value, str):
            return False
        return value in cls._value2member_map_
