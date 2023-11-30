from nazca4sdk.sdk import SDK

sdk = SDK()

print(sdk.modules)

print(sdk.variables)

# df = sdk.variable_over_time('BCM', ['vRmsy'], 10, 'MINUTE')
# df = sdk.variable_over_time('symulator', ['V1'], 3, 'HOUR')
# df = sdk.variable_over_day("symulator", ["Q2"], "2022-10-18T07:34:41", "2022-10-18T09:00:00")
# # df = sdk.variable_over_time("symulator", ["Q2"], 3, "HOUR")
# print(df)

result = sdk.read_historical_variable(module_name='symulator',
                                      variable_names=['I3'],
                                      start_date='2022-11-01T00:00:00',
                                      end_date='2022-12-17T00:00:00',
                                      page_size=1000)
if result:
    page = 1
    for a in result:
        print(f"page={page} ---> {a}")
        page = page + 1
else:
    print(f"Result empty")
