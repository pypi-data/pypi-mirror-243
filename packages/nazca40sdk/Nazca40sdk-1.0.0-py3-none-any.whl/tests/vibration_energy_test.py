from nazca4sdk.sdk import SDK

sdk = SDK(False)

if ('vRmsx' and 'vRmsy' and 'vRmsz') in sdk.variables.list()['symulator666']:
    vibration = sdk.analytics.vibration.calculate_vibration_quality('G2f', 'symulator666')
else:
    vibration = sdk.analytics.vibration.calculate_vibration_quality_by_params(group="G1r", vibration=10.0)
print(f'vibration = {vibration}')

energy = sdk.analytics.energy.calculate_energy_quality('symulator')
print('--------------------------')
print("energy from module: ", energy)


energy = sdk.analytics.energy.calculate_energy_quality('brain_test')
print(energy)

vibration = sdk.analytics.vibration.calculate_vibration_quality(module="brain_test",
                                                                group="G1r")
print(vibration)