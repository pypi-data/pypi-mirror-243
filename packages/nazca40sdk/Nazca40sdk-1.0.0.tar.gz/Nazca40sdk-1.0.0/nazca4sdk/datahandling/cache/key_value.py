from pydantic import BaseModel, StrictStr, validator


class KeyValue(BaseModel):
    key: StrictStr
    value: object

    @validator('value')
    def validate_key(cls, valid_value):
        if isinstance(valid_value, str) or isinstance(valid_value, int) or isinstance(valid_value, float):
            return valid_value
        raise ValueError('value should be string, int or float')
