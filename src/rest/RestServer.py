#!/usr/bin/python3

import json
import db.EqFetch as eqfetch
from schedule.TaskRunner import task_list
import bottle


app = bottle.default_app()


@app.route('/')
def get_all():
    data = {}

    data['status'] = 'online'
    data['equipment'] = {}
    _eq = data['equipment']
    _eq['vents'] = {}
    _eq['heaters'] = {}
    _eq['temps'] = {}
    _eq['rh_sensors'] = {}

    for id, vent in eqfetch.get_vents().items():
        _eq['vents'][id] = vent.export_dict()

    for id, heater in eqfetch.get_heaters().items():
        _eq['heaters'][id] = heater.export_dict()

    for id, temp in eqfetch.get_temps().items():
        _eq['temps'][id] = temp.export_dict()

    for id, rh_sensor in eqfetch.get_rh_sensors().items():
        _eq['rh_sensors'][id] = rh_sensor.export_dict()

    data['running_tasks'] = {}
    _rt = data['running_tasks']
    for task in task_list:
        _rt[task.name] = task.export_dict()

    return json_resp(data)


def json_resp(data):
    return json.dumps(data,
                      indent=4,
                      sort_keys=True,
                      default=str) + "\n"


def serve_forever():
    bottle.run(app, host='0.0.0.0', port=9999, debug=True)
