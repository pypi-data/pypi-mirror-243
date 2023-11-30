from nazca4sdk.energy_quality import get_energy_quality
from nazca4sdk.energy_quality import EnergyInfo
import json

data = {'freq1': 50,
        "vol1": 230,
        "cos1": 1,
        "thd1": 0,
        "freq2": 50,
        "vol2": 230,
        "cos2": 1,
        "thd2": 0,
        "freq3": 50,
        "vol3": 230,
        "cos3": 1,
        "thd3": 0}

date = EnergyInfo(freq1=50, vol1=230, cos1=1, thd1=1, freq2=50, vol2=230, cos2=1, thd2=0, freq3=50, vol3=230, cos3=1,
                  thd3=0)

print(date)
EQ = get_energy_quality(
    EnergyInfo(freq1=50, vol1=230, cos1=1, thd1=1, freq2=50, vol2=230, cos2=1,
               thd2=0, freq3=50, vol3=230, cos3=1, thd3=0))

result = {'worstCaseQuality': EQ['worstCaseQuality'],
          'worstCaseQuality1': EQ['worstCaseQuality1'],
          'worstCaseQuality2': EQ['worstCaseQuality2'],
          'worstCaseQuality3': EQ['worstCaseQuality3'],
          'volQuality1': EQ['volQuality1'],
          'volQuality2': EQ['volQuality2'],
          'volQuality3': EQ['volQuality3'],
          'cosQuality1': EQ['cosQuality1'],
          'cosQuality2': EQ['cosQuality2'],
          'cosQuality3': EQ['cosQuality3'],
          'thdQuality1': EQ['thdQuality1'],
          'thdQuality1': EQ['thdQuality2'],
          'thdQuality1': EQ['thdQuality3']
          }
print(result)

# print(type(json.dumps(result)))
# time_usage = 'Time usage is equal: {}'.format(a)
# print(time_usage)
# print(b)
# print(c)