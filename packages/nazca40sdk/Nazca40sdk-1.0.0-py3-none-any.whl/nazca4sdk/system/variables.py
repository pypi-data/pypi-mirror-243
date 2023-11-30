import pandas as pd
from datetime import datetime
from typing import Optional
from pandas import DataFrame
from nazca4sdk.datahandling.hotstorage.clickhouse.clickhouse_client import ClickhouseClient
from nazca4sdk.datahandling.hotstorage.query import Query
from nazca4sdk.datahandling.variable_verificator import VariableIntervalInfo, DATE_TIME_FORMAT, \
    VariableIntervalSubtractionInfo, VariableOverDayValidator
from nazca4sdk.system.system_cache import SystemCache
from nazca4sdk.tools.time import get_time_delta
from nazca4sdk.datahandling.data_mod import Data
from dependency_injector.wiring import inject


class Variables:
    """ Class to get module variable values

    """
    @inject
    def __init__(self, cache: SystemCache, click: ClickhouseClient):
        self._system_cache = cache
        self._clickhouse_client = click

    def list(self):
        """ List all module variables in system

        Returns:
            list: modules list
        """
        return self._system_cache.variables

    def read(self, module_name: str, variable_names: list, **time: dict) -> Optional[DataFrame]:
        """
        Gets module variables values in specific time range

        Args:
            module_name: name of module,
            variable_names: list of variable names,
            time: possible pairs - start_date, end_date or time_amount, time_unit

        Returns:
            DataFrame: values for selected variables and time range

        Examples:
            read(module_name:"module", variable_names:["V1"], start_date="2023-03-21TOO:OO:00")
            read(module_name:"module", variable_names:["V1"],time_amount=1,time_unit="MINUTE")
        """
        keys = time.keys()

        columns_to_validate = {'module_name': module_name,
                               'variable_names': variable_names}
        columns_info = VariableOverDayValidator(**columns_to_validate)

        if "start_date" in keys and "end_date" in keys:
            time_to_validate = {'start_date': time.get("start_date"),
                                'end_date': time.get("end_date")}

            time_info = VariableIntervalInfo(**time_to_validate)
            return self._variable_over_day(columns_info.module_name,
                                           columns_info.variable_names,
                                           datetime.strptime(time_info.start_date, DATE_TIME_FORMAT),
                                           datetime.strptime(time_info.end_date, DATE_TIME_FORMAT))
        elif "time_amount" in keys and "time_unit" in keys:
            time_amount = time.get("time_amount")
            time_unit = time.get("time_unit")

            time_to_validate = {'time_amount': time_amount,
                                'time_unit': time_unit}

            variable_info = VariableIntervalSubtractionInfo(**time_to_validate)

            end_date = datetime.now()
            start_date = end_date - get_time_delta(variable_info.time_unit, variable_info.time_amount)

            return self._variable_over_day(columns_info.module_name,
                                           columns_info.variable_names,
                                           start_date,
                                           end_date)

        print("time should contains start_date and end_date or time_unit and time_amount")
        return None

    def pivot(self, module_name: str, variable_names: list, **time: dict):
        dataframe = self.read(module_name, variable_names, **time)
        return 'Empty dataframe' if dataframe is None else Data(dataframe).to_pivot_df()

    def stats(self, module: str, variables: [str], start_date: str, end_date: str) -> Optional[DataFrame]:
        """ Read module variables stats

        Args:
            module: module name
            variables: list of variable names
            start_date: start of date range
            end_date: end of date range
        Returns:
            DataFrame:  Variables Stats
        """
        return self._read_variables_stats(module=module, variables=variables, start_date=start_date, end_date=end_date)

    def _read_variables_stats(self, module: str, variables: [str], start_date: str, end_date: str) \
            -> Optional[DataFrame]:
        exist_vars = self._system_cache.check_if_exist(module, variables)
        if not exist_vars:
            return None
        variables_grouped = self._system_cache.group_variables(module, variables)
        # check variables type
        for element in variables_grouped:
            if element[0] not in self._system_cache.stats_variable_type:
                print("Variable to count stats should be type of:")
                for element_type in self._system_cache.stats_variable_type:
                    print(f" -  {element_type}")
                print(f"Variables {element[1]} is type of {element[0]}")
                return None

        dataframe = pd.DataFrame()
        for key, value in variables_grouped:
            variables_list = ",".join([f"'{item}'" for item in value])
            query = Query() \
                .SELECT("Module, Variable, toFloat32(min(Value)) as Min, "
                        "toFloat32(max(Value)) as Max, toFloat64(avg(Value)) as Avg, "
                        "toFloat32(any(Value)) as FirstValue, "
                        "toFloat32(anyLast(Value)) as LastValue, toFloat64(varPop(Value)) as Variance, "
                        "toFloat64(stddevPop(Value)) as Std ") \
                .FROM(f"nazca.devices_data_{key}") \
                .WHERE(f"Module like '{module}' and "
                       f"MeasureTime >= '{start_date}' "
                       f"and MeasureTime <= '{end_date}' "
                       f"and Variable IN ({variables_list})") \
                .GROUP_BY("Module, Variable")
            df = self._clickhouse_client.get(query)
            dataframe = pd.concat([dataframe, df])
        return dataframe

    def _variable_over_day(self, module_name, variable_names, start_date, end_date) -> Optional[DataFrame]:
        """
        Gets variable in specific time range by connection with open database

        Args:
            module_name - name of module,
            variable_names - list of variable names,
            start_time - beginning of the time range
            stop_time - ending of the time range

        Returns:
            DataFrame: values for selected variable and time range

        """

        try:
            exist_vars = self._system_cache.check_if_exist(module_name, variable_names)
            if not exist_vars:
                return None
            variables_grouped = self._system_cache.group_variables(
                module_name, variable_names)

            dataframe = pd.DataFrame()
            for group in variables_grouped:
                table = group[0]
                variables = ",".join([f"'{item}'" for item in group[1]])
                query = Query() \
                    .SELECT("*") \
                    .FROM(f"nazca.devices_data_{table}") \
                    .WHERE(f"Module like '{module_name}' "
                           f"and MeasureTime >= '{start_date.strftime('%Y-%m-%dZ%H:%M:%S')}' "
                           f"and MeasureTime <= '{end_date.strftime('%Y-%m-%dZ%H:%M:%S')}' "
                           f"and Variable IN ({variables})")
                df = self._clickhouse_client.get(query)
                try:
                    dataframe = pd.concat([dataframe, df]).sort_values('MeasureTime').reset_index(drop=True)
                except:
                    raise ValueError("No data")
            return dataframe
        except ValueError:
            print("Error - Get variable data from Nazca4")
            return None
