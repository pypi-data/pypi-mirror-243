from nazca4sdk.datahandling.variable_verificator import VariableIntervalInfo
from pydantic import validator

MAX_PAGE_SIZE = 10000


class VariableHistoricalInfo(VariableIntervalInfo):
    """
    Class to verify the correctness of data for sdk.read_historical_variable range
    when start and end date is set

    Attributes:
        module parameters: dict
    """
    page_size: int = MAX_PAGE_SIZE
    page_number: int = 1

    @validator('page_size')
    def page_size_validator(cls, valid_page_size):
        if valid_page_size > MAX_PAGE_SIZE:
            raise ValueError(f"Page size can be max {MAX_PAGE_SIZE}")
        return valid_page_size
