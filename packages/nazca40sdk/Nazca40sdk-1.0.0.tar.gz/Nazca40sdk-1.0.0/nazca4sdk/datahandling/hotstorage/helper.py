from nazca4sdk.datahandling.hotstorage.model.user_variable import UserVariable, UserVariableInfo
from nazca4sdk.datahandling.hotstorage.model.user_variable import UserVariableDataType
from nazca4sdk.datahandling.hotstorage.user_variable_value import UserVariableValue
from nazca4sdk.datahandling.hotstorage.user_variable_value import user_variable_data_types
from nazca4sdk.datahandling.hotstorage.user_variables_info_value import UserVariableInfoValue

table_name_dict = {
    "bool": "bool",
    "int": "int",
    "double": "float",
    "text": "string",
    "datetime": "datetime"}

userVariableDataTypeNames = {
    UserVariableDataType.BOOL: "bool",
    UserVariableDataType.INT: "int",
    UserVariableDataType.DOUBLE: "double",
    UserVariableDataType.TEXT: "text",
    UserVariableDataType.DATETIME: "datetime"}

userVariableTableNames = {
    UserVariableDataType.BOOL: "bool",
    UserVariableDataType.INT: "int",
    UserVariableDataType.DOUBLE: "float",
    UserVariableDataType.TEXT: "string",
    UserVariableDataType.DATETIME: "datetime"
}


def get_variable_table_name(user_variable_data_type: UserVariableDataType):
    if user_variable_data_type in userVariableTableNames:
        return userVariableTableNames[user_variable_data_type]
    return None


def transform(user_variables: [UserVariable]):
    variables = []
    for user_variable in user_variables:
        try:
            user_variable_data_type = userVariableDataTypeNames[user_variable.type]
            new_var = UserVariableValue(name=user_variable.name,
                                        type=user_variable_data_type,
                                        dateTime=user_variable.datetime,
                                        value=user_variable.value)
            variables.append(new_var)
        except KeyError as e:
            print(f"UserVariableInfo(name={user_variable.name}) type error. Type {e} not supported")
    return variables


def get_table_name(data_type: str):
    try:
        table = table_name_dict[data_type]
        return table
    except KeyError:
        return ""


def transform_info(user_variables: [UserVariableInfo]):
    variables = []
    for user_variable_info in user_variables:
        try:
            user_variable_data_type = userVariableDataTypeNames[user_variable_info.type]
            new_var = UserVariableInfoValue(name=user_variable_info.name,
                                            type=user_variable_data_type)
            variables.append(new_var)
        except KeyError as e:
            print(f"UserVariableInfo(name={user_variable_info.name}) type error. Type {e} not supported")
    return variables


def create_variables_frame(user_variables: [UserVariableValue]):
    variables_frame = []
    for variable_type in user_variable_data_types:
        data_type_variables = filter(lambda x: x.type == variable_type, user_variables)
        variables_list = list(data_type_variables)
        if len(variables_list) > 0:
            variables_data = []
            table_name = get_table_name(variable_type)
            if not table_name:
                return ""

            variables_info = {"tableName": f"user_data_{table_name}", "data": variables_data}
            for el in variables_list:
                e = [el.dateTime.strftime("%Y-%m-%dT%H:%M:%S.%f"),
                     el.dateTime.strftime("%Y-%m-%dT%H:%M:%S"),
                     el.name]
                if variable_type == "bool":
                    e.append(str(int(el.value)))
                else:
                    e.append(str(el.value))

                variables_data.append(e)
            variables_frame.append(variables_info)
    return variables_frame
