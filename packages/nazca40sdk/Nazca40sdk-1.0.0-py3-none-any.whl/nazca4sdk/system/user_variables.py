import pandas as pd
from pandas import DataFrame
from typing import Optional
from nazca4sdk import UserVariableInfo, UserVariable, UserVariableDataType
from nazca4sdk.datahandling.hotstorage.clickhouse.clickhouse_client import ClickhouseClient
from nazca4sdk.datahandling.hotstorage.helper import userVariableTableNames
from nazca4sdk.datahandling.hotstorage.query import Query
from nazca4sdk.datahandling.hotstorage.user_variable_saver import UserVariableSaver
from dependency_injector.wiring import inject


class UserVariables:
    @inject
    def __init__(self, click: ClickhouseClient, user_variable_saver: UserVariableSaver):
        self._clickhouse_client = click
        self._user_variables_saver = user_variable_saver

    def read(self, variables: [UserVariableInfo], start_date: str, end_date: str) -> DataFrame:
        """Read user variables from hot storage

               Args:
                   start_date: begin of time range
                   end_date: end of time range
                   variables: list of user variables to read

               Returns:
                   DataFrame with variables values
               """
        grouped_variables = dict()
        for d in variables:
            variables_type = userVariableTableNames[d.type]
            if variables_type not in grouped_variables.keys():
                grouped_variables[variables_type] = [d.name]
            else:
                grouped_variables[variables_type].append(d.name)

        dataframe = pd.DataFrame()
        for table in grouped_variables:
            variables_list = ",".join([f"'{item}'" for item in grouped_variables[table]])
            query = Query() \
                .SELECT("*") \
                .FROM(f"nazca.user_data_{table}") \
                .WHERE(f"DateTime >= '{start_date}' "
                       f"and DateTime <= '{end_date}' "
                       f"and Variable IN ({variables_list})")
            df = self._clickhouse_client.get(query)
            dataframe = pd.concat([dataframe, df])
        return dataframe

    def write(self,  user_variables: [UserVariable]) -> bool:
        """
        Save user variables in hot storage

        Args:
            user_variables: list of user variables to save

        Returns:
            True - variables to save send to hot storage
            False - communication with hot storage error
        """

        return self._user_variables_saver.save_variables(user_variables)

    def stats(self, variables: [UserVariableInfo], start_date: str, end_date: str) -> Optional[DataFrame]:
        """Read user variables stats

           Args:
               variables: list of variables names
               start_date: start of date range
               end_date: end of date range
           Returns:
               VariableStats DataFrame
        """

        if not isinstance(variables, list):
            print("variables should be list")
            return None
        grouped_variables = dict()
        for d in variables:
            if d.type == UserVariableDataType.TEXT or d.type == UserVariableDataType.BOOL:
                print(f"user_variables_stats only for INT and DOUBLE type, not for {d.type}")
                continue
            variables_type = userVariableTableNames[d.type]
            if variables_type not in grouped_variables.keys():
                grouped_variables[variables_type] = [d.name]
            else:
                grouped_variables[variables_type].append(d.name)

        dataframe = pd.DataFrame()
        for table in grouped_variables:
            variables_list = ",".join([f"'{item}'" for item in grouped_variables[table]])
            query = Query() \
                .SELECT("Variable, toFloat32(min(Value)) as Min, "
                        "toFloat32(max(Value)) as Max, toFloat64(avg(Value)) as Avg, "
                        "toFloat32(any(Value)) as FirstValue, "
                        "toFloat32(anyLast(Value)) as LastValue, toFloat64(varPop(Value)) as Variance, "
                        "toFloat64(stddevPop(Value)) as Std ") \
                .FROM(f"nazca.user_data_{table}") \
                .WHERE(f"DateTime >= '{start_date}' "
                       f"and DateTime <= '{end_date}' "
                       f"and Variable IN ({variables_list})") \
                .GROUP_BY("Variable")
            df = self._clickhouse_client.get(query)
            dataframe = pd.concat([dataframe, df])
        return dataframe
