from nazca4sdk import UserVariableInfo, UserVariableDataType
from nazca4sdk.sdk import SDK

sdk = SDK()
#
# sdk.modules
# sdk.variables

print(f"Modules={sdk.modules}")
print(f"Varaibles={sdk.variables.list()}")
# print(sdk.user_variables.read([UserVariableInfo(UserVariableDataType.INT, "I1")], '2023-10-16T00:00:00', '2023-10-16T23:00:00'))
#print(sdk.read_variables_stats('symulator', ['P1', 'Q1'], '2023-01-24T00:00:00', '2023-01-24T23:00:00'))

print(sdk.cache.read_keys(["dupa"]))