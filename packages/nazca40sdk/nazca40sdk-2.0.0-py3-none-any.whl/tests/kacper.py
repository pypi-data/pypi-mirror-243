from nazca4sdk.sdk import SDK

sdk = SDK(False)
sdk.modules
# print(sdk.read_by_query(query='SELECT * FROM nazca.devices_data_int LIMIT 200'))
print(sdk.read_by_query(query='SELECT Module, MeasureTimeLong, MeasureTime, MeasureDate, Variable, Value FROM nazca.devices_data_int order by MeasureTimeLong desc LIMIT 100;'))
# print(list('SELECT * FROM nazca.test LIMIT 5'))
