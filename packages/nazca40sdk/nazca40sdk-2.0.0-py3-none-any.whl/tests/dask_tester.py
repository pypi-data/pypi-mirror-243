from nazca4sdk.sdk import SDK
import time

sdk = SDK(False)

start_time = time.time()
data = sdk.variable_over_time('symulator', ['V1'], 15, 'DAY')
print(data)
print(type(data))
print("--- %s seconds ---" % round((time.time() - start_time), 2))
print(len(data))

start_time = time.time()
dask_data = sdk.variable_over_time('symulator', ['V1'], 15, 'DAY', dask=True)
print('----------------------')
print(dask_data)
print(type(dask_data))
print("--- %s seconds ---" % round((time.time() - start_time), 2))
print(len(dask_data))
print(dask_data.head(10))

start_time = time.time()
data_day = data = sdk.variable_over_day('symulator', ['V1'], '2023-01-15T07:00:00', '2023-02-06T07:30:00')
print('----------------------')
print(data_day)
print(type(data_day))
print("--- %s seconds ---" % round((time.time() - start_time), 2))
print(len(data_day))

start_time = time.time()
data_dask_day = sdk.variable_over_day('symulator', ['V1'], '2023-01-15T07:00:00', '2023-02-06T07:30:00', dask=True)
print('----------------------')
print(data_dask_day)
print(type(data_dask_day))
print("--- %s seconds ---" % round((time.time() - start_time), 2))
print(len(data_dask_day))
print(data_dask_day.head(10))

