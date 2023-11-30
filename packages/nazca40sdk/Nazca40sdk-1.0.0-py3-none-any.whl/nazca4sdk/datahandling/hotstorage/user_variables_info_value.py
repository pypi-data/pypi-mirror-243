from datetime import datetime

from pydantic import BaseModel, validator

types = ["bool", "int", "double", "datetime", "text"]
DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATE_TIME_EXAMPLE = "yyyy-mm-ddTHH:MM:SS"


class UserVariableInfoValue(BaseModel):
    type: str
    name: str

    @validator("type")
    def validate_type(cls, valid_type):
        if valid_type not in types:
            raise ValueError(f"type should be one of {types}")
        return valid_type


class UserVariablesInfoValues(BaseModel):
    variables = {}
    startDate: str
    endDate: str

    @validator("endDate")
    def validate_end_date(cls, valid_datetime):
        """Validator to check if time amount is correct

               Args:
                   valid_datetime: str

               Returns:
                   valid_datetime: str
               """
        try:
            datetime.strptime(valid_datetime, DATE_TIME_FORMAT)
            return valid_datetime
        except ValueError:
            raise ValueError(
                f'Bad datetime format. Example {DATE_TIME_EXAMPLE} ')

    @validator("startDate")
    def valid_start_date(cls, valid_datetime):
        """Validator to check if time amount is correct

        Args:
            valid_datetime: str

        Returns:
            valid_datetime: str
        """
        try:
            datetime.strptime(valid_datetime, DATE_TIME_FORMAT)
            return valid_datetime
        except ValueError:
            raise ValueError(
                f'Bad datetime format. Example {DATE_TIME_EXAMPLE}')

    def add_variable(self, variable: UserVariableInfoValue):

        if variable.type not in self.variables:
            self.variables[variable.type] = []
        self.variables[variable.type].append(variable.name)

    @staticmethod
    def valid_datetime(valid_datetime):
        """Validator to check if time amount is correct

        Args:
            valid_datetime: str

        Returns:
            valid_datetime: str
        """
        try:
            datetime.strptime(valid_datetime, DATE_TIME_FORMAT)
            return valid_datetime
        except ValueError:
            raise ValueError(
                f'Bad datetime format. Format {DATE_TIME_EXAMPLE}')
