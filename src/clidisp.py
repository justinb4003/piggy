#!/usr/bin/python3

import requests

resp = requests.get("http://localhost:9999/")
print(resp.content)
data = resp.json()
eq = data['equipment']
for h in eq['heaters']:
    print("{} : {}".format(eq['heaters'][h]['long_name'],
                           eq['heaters'][h]['is_on']))
for v in eq['vents']:
    print("{} : {}%".format(eq['vents'][v]['long_name'],
                            eq['vents'][v]['current_percent']))
for c in eq['curtains']:
    print("{} : {}%".format(eq['curtains'][c]['long_name'],
                            eq['curtains'][c]['current_percent']))
    # TODO: Figure out why this doesn't work.
    # I'm missing something stupid here.
    # print("h IS: {}".format(h['is_on']))
