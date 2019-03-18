import json
import db.EqFetch as eqfetch
import schedule.TaskRunner as tr
import bottle


app = bottle.default_app()


@app.route('/tasks/load')
def tasks_load():
    # Reload tasks from database
    tr.load_tasks()


@app.route('/tasks/save')
def tasks_save():
    # Save tasks back to database
    tr.save_tasks()


@app.route('/tasks/del/<uuid>')
def tasks_del(uuid):
    tr.del_task(uuid)
    pass


@app.route('/tasks/add')
def tasks_add(uuid):
    # Get data from the JSON payload
    pass


@app.route('/tasks/running')
def tasks_running():
    return json_resp(get_running_tasks())


@app.route('/tasks/avail')
def tasks_avail():
    return json_resp(get_avail_tasks())


@app.route('/equipment/heaters')
def equipment_heaters():
    return json_resp(get_heaters())


@app.route('/equipment/vents')
def equipment_vents():
    return json_resp(get_vents())


@app.route('/equipment/curtains')
def equipment_curtains():
    return json_resp(get_curtains())


# I might currently think my earlier decision to make Sensors also
# Subsystems and thereby lump them all in 'subsystems' was dumb
# but we don't have to expose the sensors like other equipment to the
# application integrators, so here's where we fix that.
@app.route('/sensors/temp')
def sensors_temp():
    return json_resp(get_temps())


@app.route('/sensors/rh')
def sensors_rh():
    return json_resp(get_rh_sensors())


@app.route('/sensors/sun')
def sensors_sun():
    return json_resp(get_sun_sensors())


@app.route('/sensors/wind')
def sensors_wind():
    return json_resp(get_wind_sensors())


@app.route('/')
def get_all():
    data = {}

    data['status'] = 'online'
    data['equipment'] = {}
    _eq = data['equipment']
    _eq['vents'] = get_vents()
    _eq['heaters'] = get_heaters()
    _eq['curtains'] = get_curtains()
    _eq['temps'] = get_temps()
    _eq['rh_sensors'] = get_rh_sensors()
    _eq['sun_sensors'] = get_sun_sensors()
    _eq['wind_sensors'] = get_wind_sensors()

    data['running_tasks'] = get_running_tasks()

    return json_resp(data)


def get_wind_sensors():
    ret = {}
    for id, wind_sensor in eqfetch.get_wind_sensors().items():
        ret[id] = wind_sensor.export_dict()
    return ret


def get_sun_sensors():
    ret = {}
    for id, sun_sensor in eqfetch.get_sun_sensors().items():
        ret[id] = sun_sensor.export_dict()
    return ret


def get_rh_sensors():
    ret = {}
    for id, rh_sensor in eqfetch.get_rh_sensors().items():
        ret[id] = rh_sensor.export_dict()
    return ret


def get_temps():
    ret = {}
    for id, temp in eqfetch.get_temps().items():
        ret[id] = temp.export_dict()
    return ret


def get_curtains():
    ret = {}
    for id, curtain in eqfetch.get_curtains().items():
        ret[id] = curtain.export_dict()
    return ret


def get_vents():
    ret = {}
    for id, vent in eqfetch.get_vents().items():
        ret[id] = vent.export_dict()
    return ret


def get_heaters():
    ret = {}
    for id, heater in eqfetch.get_heaters().items():
        ret[id] = heater.export_dict()
    return ret


def get_running_tasks():
    ret = {}
    for task in tr.get_tasks():
        d = task.export_as_dict()
        # Add in some of the top-level config options for tasks
        d['uuid'] = task.uuid
        d['name'] = task.name
        d['priority'] = task.priority
        print("adding task dict to rest server: {}".format(d))
        ret[task.uuid] = d
    return ret


def get_avail_tasks():
    return tr.get_avail_tasks()


def json_resp(data):
    return json.dumps(data,
                      indent=4,
                      sort_keys=True,
                      default=str) + "\n"


def serve_forever():
    bottle.run(app, host='0.0.0.0', port=9999, debug=True)
