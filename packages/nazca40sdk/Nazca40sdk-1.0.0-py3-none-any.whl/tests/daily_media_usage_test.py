from nazca4sdk.sdk import SDK
import datetime as dat
from datetime import datetime as dt

sdk = SDK(False)

# start_date = f'{dat.date.today()}T00:00:00Z'
# end_date = f'{dat.date.today()}T{dt.now().strftime("%H:%M:%S")}Z'
#
# print(start_date)
# print (end_date)

print(sdk.variables)
# #
print(sdk.daily_media_usage('SD5500_Fanuc', 'Zuzycie'))
# #
print(sdk.daily_energy_usage('Socomec_LiniaD1'))

# print(sdk.variable_over_time('symulator', ['Ea_dec'], 1, 'DAY'))

print(sdk.daily_media_usage('symulator', 'Ea_dec'))
