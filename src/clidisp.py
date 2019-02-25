#!/usr/bin/python3

import requests

resp = requests.get("http://localhost:9999/")
data = resp.json()
print(data)
eq = data['equipment']
for h in eq['heaters']:
    print("{} : {}".format(eq['heaters'][h]['long_name'],
                           eq['heaters'][h]['is_on']))
for v in eq['vents']:
    print("{} : {}%".format(eq['vents'][v]['long_name'],
                            eq['vents'][v]['current_percent']))
    # TODO: Figure out why this doesn't work.
    # I'm missing something stupid here.
    # print("h IS: {}".format(h['is_on']))
