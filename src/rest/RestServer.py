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


@app.route('/')
def get_all():
    data = {}

    data['status'] = 'online'
    data['equipment'] = {}
    _eq = data['equipment']
    _eq['vents'] = {}
    _eq['heaters'] = {}
    _eq['curtains'] = {}
    _eq['temps'] = {}
    _eq['rh_sensors'] = {}
    _eq['sun_sensors'] = {}

    for id, vent in eqfetch.get_vents().items():
        _eq['vents'][id] = vent.export_dict()

    for id, heater in eqfetch.get_heaters().items():
        _eq['heaters'][id] = heater.export_dict()

    for id, curtain in eqfetch.get_curtains().items():
        _eq['curtains'][id] = curtain.export_dict()

    for id, temp in eqfetch.get_temps().items():
        _eq['temps'][id] = temp.export_dict()

    for id, rh_sensor in eqfetch.get_rh_sensors().items():
        _eq['rh_sensors'][id] = rh_sensor.export_dict()

    for id, sun_sensor in eqfetch.get_sun_sensors().items():
        _eq['sun_sensors'][id] = sun_sensor.export_dict()

    data['running_tasks'] = get_running_tasks()

    return json_resp(data)


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
