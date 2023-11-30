"""Variable verification module"""
from datetime import datetime
from typing import Optional, List
import sys
from pydantic import BaseModel, validator

DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"


class ElectricMetersDataValidator(BaseModel):
    """Class to verify the correctness of data for get_electric_meters_data function

    Attributes:
    system_name: List[str]
    variables: List[str]
    """
    system_name: List[str]
    variables: List[str]


class PgAvgDataValidator(BaseModel):
    """Class to verify the correctness of data for get_pgavg_data function

    Attributes:
    connection: str
    start_date: str
    end_date: str
    """
    connection: str
    start_date: str
    end_date: str

    @validator('start_date')
    def start_date_verify_format(cls, valid_start_date):
        """Validator to check if start_date is correct

        Args:
            valid_start_date: str

        Returns:
            valid_start_date: str
        """
        return PgAvgDataValidator.valid_datetime(valid_start_date)

    @validator('end_date')
    def end_date_verify_format(cls, valid_end_date, values):
        """Validator to check if end_date is correct

        Args:
            valid_end_date: str
            values : str
        Returns:
            valid_end_date: str
        """
        PgAvgDataValidator.valid_datetime(valid_end_date)
        if 'start_date' in values:
            start_date_str = values['start_date']
            end_date = datetime.strptime(valid_end_date, DATE_TIME_FORMAT)
            start_date = datetime.strptime(start_date_str, DATE_TIME_FORMAT)
            if end_date > start_date:
                return valid_end_date
            raise ValueError(
                f'{valid_end_date} must be after {start_date_str}')
        raise ValueError('Cannot check if end_date is after start_date')

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
                'Bad datetime format. Format yyyy-mm-ddTHH:MM:SS')


class SsvSopOrderedPowerDataValidator(BaseModel):
    """Class to verify the correctness of data for get_ssv_sop_orderedpower function

    Attributes:
    connection: str
    """
    connection: str


class OrganizationCo2DataValidator(BaseModel):
    """Class to verify the correctness of data for get_organization_co2 function

    Attributes:
    organization_id: str
    """
    organization_id: str


class OzeConnectionInvertersDataValidator(BaseModel):
    """Class to verify the correctness of data for get_oze_connection_inverters function

    Attributes:
    connection_id: str
    """
    connection_id: str


class OzeConnectionsForMetersDataValidator(BaseModel):
    """Class to verify the correctness of data for get_oze_connections_for_meters function

    Attributes:
    meters: list
    """
    meters: list


class OzeInvertersSummaryDataValidator(BaseModel):
    """Class to verify the correctness of data for get_inverters_summary_data function

    Attributes:
    inverters: list
    from_date: str
    to_date: str
    """
    inverters: list
    from_date: str
    to_date: str


class MetersDataValidator(BaseModel):
    """Class to verify the correctness of data for get_meters_data function

    Attributes:
    meters: list
    from_date: str
    to_date: str
    """
    meters: list
    from_date: str
    to_date: str


class VariableOverDayValidator(BaseModel):
    """Class to verify the correctness of data for variable_over_day function

    Attributes:
    module_name: str
    variable_names: list
    """
    module_name: str
    variable_names: list


class VariableIntervalInfo(VariableOverDayValidator):
    """Class to verify the correctness of data for variable over time range
    when start and end date is set

    Attributes:
        module parameters: dict
    """
    start_date: str
    end_date: str

    @validator('start_date')
    def start_date_verify_format(cls, valid_start_date):
        """Validator to check if time amount is correct

        Args:
            valid_start_date: str

        Returns:
            valid_start_date: str
        """
        return VariableIntervalInfo.valid_datetime(valid_start_date)

    @validator('end_date')
    def end_date_verify_format(cls, valid_end_date, values):
        """Validator to check if time amount is correct

        Args:
            valid_end_date: str
            values : str
        Returns:
            valid_end_date: str
        """
        VariableIntervalInfo.valid_datetime(valid_end_date)
        if 'start_date' in values:
            start_date_str = values['start_date']
            end_date = datetime.strptime(valid_end_date, DATE_TIME_FORMAT)
            start_date = datetime.strptime(start_date_str, DATE_TIME_FORMAT)
            if end_date > start_date:
                return valid_end_date
            raise ValueError(
                f'{valid_end_date} must be after {start_date_str}')
        raise ValueError('Cannot check if end_date is after start_date')

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
                'Bad datetime format. Format yyyy-mm-ddTHH:MM:SS')


class VariableIntervalSubtractionInfo(BaseModel):
    """Class to verify the correctness of data for variable over time range
     when time unit and time amount is set

    Attributes:
        time parameters: dict
    """
    time_unit: str
    time_amount: int

    @validator('time_amount')
    def time_amount_validator(cls, valid_time_amount):
        """
        Validator to check if time amount is correct

        Args:
            valid_time_amount: int

        Returns:
            valid_time_amount: int
        """
        if 0 >= valid_time_amount > sys.maxsize:
            raise ValueError('time_amount has to be greater than 0')
        return valid_time_amount

    @validator('time_unit')
    def time_unit_validator(cls, valid_time_unit):
        """Validator to check if time unit is correct

        Args:
            valid_time_unit: str

        Returns:
            valid_time_unit: str
        """
        possibilities = ['SECOND', 'MINUTE',
                         'HOUR', 'DAY', "MONTH", 'WEEK', 'YEAR']
        if valid_time_unit not in possibilities:
            raise ValueError(
                'Wrong time aggregator, try: SECOND, MINUTE, HOUR, DAY, WEEK, YEAR')
        return valid_time_unit


class OeeSimpleParams(BaseModel):
    """Class to verify the correctness of data for Simple OEE function

    Attributes:
    availability: float
    performance: float
    quality: float
    """
    availability: float
    performance: float
    quality: float

    @validator('availability')
    def availability_validator(cls, value):
        """ Availability parameter validator """
        if value < 0:
            raise ValueError('Availability has to be higher than')
        return float(value)

    @validator('performance')
    def performance_validator(cls, value):
        """ Performance parameter validator """
        if value < 0:
            raise ValueError('Performance has to be higher than')
        return float(value)

    @validator('quality')
    def quality_validator(cls, value):
        """Quality parameter validator """
        if value < 0:
            raise ValueError('Quality has to be higher than')
        return float(value)


class OeeComplexParams(BaseModel):
    """Class to verify the correctness of data for variable OEE

    Attributes:
    A : (float) Total available time,
    B : (float) Run time,
    C : (float) Production capacity,
    D : (float) Actual production,
    E : (float) Production output (same as actual production),
    F : (float) Actual good products (i.e. product output minus scraps)
    """

    A: float
    B: float
    C: float
    D: float
    E: float
    F: float


class AvailabilityValidator(BaseModel):
    """Class to verify the correctness of data for availability

    Attributes:
    run_time: float
    total_time: float
    """
    run_time: float
    total_time: float


class PerformanceValidator(BaseModel):
    """Class to verify the correctness of data for performance

    Attributes:
    actual_production: float
    production_capacity: float
    """
    actual_production: float
    production_capacity: float


class QualityValidator(BaseModel):
    """Class to verify the correctness of data for quality

    Attributes:
    actual_products: float
    production_output: float
    """
    actual_products: float
    production_output: float


class CpCpkIndicatorsParams(BaseModel):
    """
    Class to verify the correctness of data for cp, cpk indicators

    Args:
    module: (str)
    variable: (str)
    start_date: (str)
    end_date: (str)
    lsl: (float)
    usl: (float)
    period: (int)
    subgroups: (int)
    estimation_type: (str)
    """
    module: str
    variable: str
    start_date: str
    end_date: str
    lsl: Optional[float]
    usl: Optional[float]
    period: int
    subgroups: int
    estimation_type: str

    @validator('estimation_type')
    def estimation_type_validate(cls, estimation_type):
        """ estimation_type validator """
        if estimation_type != 'time' and estimation_type != 'samples':
            raise ValueError('estimation_type has to be time or samples')

        return estimation_type

    @validator('subgroups')
    def subgroups_validate(cls, subgroups):
        """ subgroups validator """
        if subgroups <= 0:
            raise ValueError('Value has to be greater than 0')

        return float(subgroups)

    @validator('period')
    def period_validate(cls, period):
        """ period validator """
        if period <= 0:
            raise ValueError('Value has to be greater than 0')

        return float(period)

    @validator('usl', pre=True, always=True)
    def limits_validate(cls, usl, values):
        """ Cpk/ppk limits validator """
        if not values.get('lsl') and not usl:
            raise ValueError('Either lsl or usl is required')

        if not usl:
            return

        if 'lsl' in values:
            lsl_value = values['lsl']

            if lsl_value is None:
                return usl
            if usl > lsl_value:
                return usl
            raise ValueError('Value has to be grater than lsl')

    @validator('start_date')
    def start_date_verify_format(cls, valid_start_date):
        """Validator to check if time amount is correct

        Args:
            valid_start_date: str

        Returns:
            valid_start_date: str
        """
        return VariableIntervalInfo.valid_datetime(valid_start_date)

    @validator('end_date')
    def end_date_verify_format(cls, valid_end_date, values):
        """Validator to check if time amount is correct

        Args:
            valid_end_date: str
            values : str
        Returns:
            valid_end_date: str
        """
        VariableIntervalInfo.valid_datetime(valid_end_date)
        if 'start_date' in values:
            start_date_str = values['start_date']
            end_date = datetime.strptime(valid_end_date, DATE_TIME_FORMAT)
            start_date = datetime.strptime(start_date_str, DATE_TIME_FORMAT)
            if end_date > start_date:
                return valid_end_date
            raise ValueError(
                f'{valid_end_date} must be after {start_date_str}')
        raise ValueError('Cannot check if end_date is after start_date')


class PpPpkIndicatorsParams(BaseModel):
    """
    Class to verify the correctness of data for pp, ppk indicators

    Attributes:
    module: (str)
    variable: (str)
    start_date: (str)
    end_date: (str)
    lsl : (float)
    usl : (float)


    """
    module: str
    variable: str
    start_date: str
    end_date: str
    lsl: Optional[float]
    usl: Optional[float]

    @validator('usl')
    def limits_validate(cls, usl, values):
        """ Cpk/ppk limits validator """
        if not values.get('lsl') and not usl:
            raise ValueError('Either lsl or usl is required')

        if not usl:
            return

        if 'lsl' in values:
            lsl_value = values['lsl']

            if lsl_value is None:
                return usl
            if usl > lsl_value:
                return usl
            raise ValueError('Value has to be grater than lsl')

    @validator('start_date')
    def start_date_verify_format(cls, valid_start_date):
        """Validator to check if time amount is correct

        Args:
            valid_start_date: str

        Returns:
            valid_start_date: str
        """
        return VariableIntervalInfo.valid_datetime(valid_start_date)

    @validator('end_date')
    def end_date_verify_format(cls, valid_end_date, values):
        """Validator to check if time amount is correct

        Args:
            valid_end_date: str
            values : str
        Returns:
            valid_end_date: str
        """
        VariableIntervalInfo.valid_datetime(valid_end_date)
        if 'start_date' in values:
            start_date_str = values['start_date']
            end_date = datetime.strptime(valid_end_date, DATE_TIME_FORMAT)
            start_date = datetime.strptime(start_date_str, DATE_TIME_FORMAT)
            if end_date > start_date:
                return valid_end_date
            raise ValueError(
                f'{valid_end_date} must be after {start_date_str}')
        raise ValueError('Cannot check if end_date is after start_date')


class VariableType(BaseModel):
    """Class to verify the type of variable names

    Attributes:
        variables_grouped: variable type
    """
    variables_grouped: list

    @validator('variables_grouped')
    def variable_verify_type(cls, variables_grouped):
        """Validator to check the value type of input variable names

        Args:
            variables_grouped: str

        Returns:
            variables_grouped: str
        """
        if variables_grouped[0][0] != 'float' and variables_grouped[0][0] != 'int':
            raise ValueError(
                'Values from input variable has to be float or int')

        return variables_grouped[0][1][0]


class ForecastForPrediction(BaseModel):
    """Class to verify the forecast time amount ant unit to make future dataframe to for prediction and verify
    prediction tool

    Attributes:
        forecast_time_amount: int
        forecast_time_unit: str
        prediction_tool: str: "prophet" or "nixtla"
    """

    forecast_time_amount: int
    forecast_time_unit: str
    prediction_tool: str

    @validator('prediction_tool')
    def prediction_tool_verify_name(cls, prediction_tool):
        """Validator to check the prediction_tool

        Args:
            prediction_tool: str

        Returns:
            prediction_tool: str
        """

        tools = ['prophet', 'nixtla']

        if prediction_tool not in tools:
            raise ValueError('prediction tool has to be "prophet" or "nixtla"')

        return prediction_tool

    @validator('forecast_time_amount')
    def forecast_time_amount_verify(cls, forecast_time_amount):
        """Validator to check the forecast_time_unit

        Args:
            forecast_time_amount: str

        Returns:
            forecast_time_amount: str
        """

        if 0 >= forecast_time_amount > sys.maxsize:
            raise ValueError('forecast_time_amount has to be greater than 0')
        return forecast_time_amount

    @validator('forecast_time_unit')
    def forecast_time_unit_verify(cls, forecast_time_unit):
        """Validator to check the forecast_time_unit

        Args:
            forecast_time_unit: str

        Returns:
            forecast_time_unit: str
        """

        units = ['Y', 'M', 'D', 'H', 'MIN', 'S']

        if forecast_time_unit.upper() not in units:
            raise ValueError("forecast time unit has to be 'Y' or 'y' (year), 'M' or 'm' (month), 'D' or 'd' (day), "
                             "'H' or 'h' (hour), 'MIN' or 'min' (minute), 'S' or 's' (second)")

        return forecast_time_unit
