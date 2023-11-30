from nazca4sdk import SDK
from nazca4sdk import UserVariable, UserVariableInfo, UserVariableDataType


u = UserVariable(UserVariableDataType.TEXT, "text", 13.2)
u1 = UserVariable(UserVariableDataType.DOUBLE, "double", 43.1)
u2 = UserVariable(UserVariableDataType.INT, "int", 127)
u3 = UserVariable(UserVariableDataType.BOOL, "bool", True)
u4 = UserVariable(UserVariableDataType.BOOL, "bool", False)
u7 = UserVariable(UserVariableDataType.INT, "int", 236)
u5 = UserVariable(UserVariableDataType.TEXT, "text", "Text1")
u6 = UserVariable(UserVariableDataType.TEXT, "tex", "Text2")
ud = UserVariable(UserVariableDataType.DATETIME, "datetime", "2022-10-04T15:05:01")

sdk = SDK(False)
# print(sdk.write_hotstorage_variables([u, u1, u2, u3, u4, u5, u6, ud]))
#
# va = UserVariableInfo(name="int", type=UserVariableDataType.INT)
# va2 = UserVariableInfo(name="text", type=UserVariableDataType.TEXT)
# res = sdk.read_hotstorage_variables("2022-10-04T00:40:02", "2022-10-05T17:00:00", [va, va2])
# print(len(res))
# for x in res:
#     print(x)
print(sdk.variables.read_variables_stats(module="symulator", variables=["V1", "V2"],
                                         start_date="2022-09-30T00:00:00", end_date="2022-10-20T00:00:00"))

v1 = UserVariableInfo(name="David", type=UserVariableDataType.INT)
v2 = UserVariableInfo(name="Ziutek", type=UserVariableDataType.INT)

print(sdk.variables.read_user_variables_stats(variables=[v1, v2],
                                              start_date="2022-09-15T00:00:00",
                                              end_date="2022-10-20T00:00:00"))
