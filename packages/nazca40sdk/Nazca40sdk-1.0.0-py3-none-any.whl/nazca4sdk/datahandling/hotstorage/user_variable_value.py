from datetime import datetime
from typing import List

from pydantic import BaseModel, StrictStr, validator

DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
user_variable_data_types = ["bool", "int", "double", "datetime", "text"]


class UserVariableValue(BaseModel):
    name: StrictStr
    type: StrictStr
    value: object
    dateTime: datetime

    @validator('value')
    def validate_key(cls, valid_value):
        if isinstance(valid_value, str) or isinstance(valid_value, int) or isinstance(valid_value, float) or isinstance(
                valid_value, bool) or isinstance(valid_value, datetime):
            return valid_value
        raise ValueError('value should be string, int or float')

    @validator('dateTime')
    def validate_datetime(cls, valid_datetime):
        if isinstance(valid_datetime, datetime):
            return valid_datetime
        if isinstance(valid_datetime, str):
            return datetime.strptime(valid_datetime)
        raise ValueError(f"{valid_datetime} is not valid datetime")

    @validator("type")
    def validate_type(cls, valid_type):
        if valid_type not in user_variable_data_types:
            raise ValueError(f"type should be one of -{user_variable_data_types}")
        return valid_type

    @validator("value")
    def validate_value(cls, valid_value, values):
        if 'type' not in values:
            raise ValueError("Can't validate value, bad type")
        data_type = values['type'].lower()
        if data_type == 'bool':
            if isinstance(valid_value, int):
                return bool(valid_value)
            if not isinstance(valid_value, bool):
                raise ValueError(f"Value {valid_value} is not bool")
            if not isinstance(valid_value, bool):
                raise ValueError(f"Value {valid_value} is not bool")
        if data_type == 'int' and ((isinstance(valid_value, bool) and isinstance(valid_value, int)) or (
                not isinstance(valid_value, bool) and not isinstance(valid_value, int))):
            raise ValueError(f"Value {valid_value} is not int")
        elif data_type == 'int' and isinstance(valid_value, int):
            if valid_value > 2147483647:
                raise ValueError(f"Value  {valid_value} is more then max int 2147483647")
            if valid_value < -2147483648:
                raise ValueError(f"Value  {valid_value} is less then min int -2147483648")
        if data_type == 'double' and (not isinstance(valid_value, float) and not isinstance(valid_value, int)):
            raise ValueError(f"Value {valid_value} is not float")
        elif data_type == 'double' and isinstance(valid_value, float):
            if valid_value > 3.4000002e38:
                raise ValueError(f"Value  {valid_value} is more then max double 3.4e38")
            if valid_value < -3.4000002e38:
                raise ValueError(f"Value  {valid_value} is less then min double -3.4e38")
        if data_type == 'datetime':
            if isinstance(valid_value, str):
                return UserVariableValue.valid_datetime(valid_value)
            if not isinstance(valid_value, datetime):
                raise ValueError(f"{valid_value} is not valid datetime")
            return valid_value
        if data_type == 'text' and not isinstance(valid_value, str):
            raise ValueError(f"value {valid_value} should be string")
        return valid_value

    @staticmethod
    def valid_datetime(valid_datetime):
        """Validator to check if time amount is correct

        Args:
            valid_datetime: str

        Returns:
            valid_datetime: str
        """
        try:
            return datetime.fromisoformat(valid_datetime)
        except ValueError:
            raise ValueError(
                f'Bad datetime format({valid_datetime}). Format should be iso8601')


class UserVariablesValues(BaseModel):
    __root__: List[UserVariableValue]

    def variables(self):
        return self.__root__
