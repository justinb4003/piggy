import importlib
import inspect
from threading import Lock

task_lock = Lock()
task_list = []


def export_dict():
    """
    Export running tasks to a dict so we can JSON format them
    """
    pass


def create_obj(obj_name):
    # TODO: Load tasks from the DB, but at least we're dynamically
    # creating them now.
    mod = importlib.import_module("task.{}".format(obj_name))
    members = dict(inspect.getmembers(mod))
    return members[obj_name]()


def load_tasks():
    """
    Pull tasks from DB and set them up to run. We want to be able to hit
    this on the fly with a running system, hence the locking.

    TODO: Actually pull them from the DB.  I'm just hard-coding them in now.
    """
    with task_lock:
        task_list.clear()
        # task_list.append(create_obj("WindLimits")('Storm Protection', -1000))
        heating_config = {}
        heating_config['name'] = 'Basic Heating'
        heating_config['priority'] = 10
        heating_config['heat1'] = 'HEAT01'
        heating_config['temp_sensor'] = 'TEMP01'
        heating_config['on_at'] = 58
        heating_config['off_at'] = 64

        cooling_config = {}
        cooling_config['name'] = 'Basic Cooling'
        cooling_config['priority'] = 20
        cooling_config['vent1'] = 'RETROOF'
        cooling_config['temp_sensor'] = 'TEMP01'
        cooling_config['on_at'] = 80
        cooling_config['off_at'] = 60
        cooling_config['crack'] = 10
        cooling_config['step'] = 15

        shading_config = {}
        shading_config['name'] = 'Basic Shading'
        shading_config['priority'] = 30
        shading_config['curtain1'] = 'RETSHADE'
        shading_config['temp_sensor'] = 'TEMP01'
        shading_config['on_at'] = 90
        shading_config['off_at'] = 60
        shading_config['max_shade'] = 50

        wl_config = {}
        wl_config['name'] = 'Storm Protection'
        wl_config['priority'] = -1000
        wl_config['vent1'] = 'RETROOF'
        wl_config['vent2'] = 'RETROOF'
        wl_config['wind_sensor'] = 'WIND'
        wl_config['max_wind'] = 25

        task_obj = create_obj("Heating")
        task_obj.import_by_dict(heating_config)
        task_list.append(task_obj)

        task_obj = create_obj("Cooling")
        task_obj.import_by_dict(cooling_config)
        task_list.append(task_obj)

        task_obj = create_obj("Shading")
        task_obj.import_by_dict(shading_config)
        task_list.append(task_obj)

        task_obj = create_obj("WindLimits")
        task_obj.import_by_dict(wl_config)
        task_list.append(task_obj)

        # task_list.append(create_obj("Heating")('Basic Heating', 10))
        # task_list.append(create_obj("Cooling")('Basic Cooling', 20))
        # task_list.append(create_obj("Shading")('Dumb Shading', 30))


def execute():
    """
    Loop through the tasks and figure out what we need to
    actually do on this iteration.
    Interval that this is hit at will be configurable, but should be
    something like 30-60 seconds.
    """
    with task_lock:
        run_queue = {}
        for task in task_list:
            # I know it looks stupid to have a different method
            # to return priority here when want_action could just do it all
            # and be cleaner.
            # The reason is, and this isn't going to happen in grenhouse
            # environmental control, is you might want to avoid calling
            # a possibly expensive want_action if we're in an situation
            # where we need to spare computing time.  Think obstacle avoidance
            # where you might not care about monitoring battery level because
            # you're not going to break off to recharge until the minor
            # emergency is over.
            # So you could say any task under 100 is an emergency and when
            # they need action anything under 1000 cut off.
            # Ok so that's a long explanation for my stupid looking code.
            # Good talk everybody.
            p = task.get_priority()
            want, eq_wanted = task.want_action()
            if want:
                run_queue[p] = (task, eq_wanted)

        # Now we figure out who gets to actually play with what...
        taken_eq = []
        for pri, rt in run_queue.items():
            print("Priority {} task {} wants...".format(pri, rt[0].name))
            for e in rt[1]:
                print(e)
                if e in taken_eq:
                    print("Can't have it though.  Taken.")
                    rt[1].remove(e)
                else:
                    taken_eq.append(e)

        # Now that we've ripped out equipment from the run_queue if a higher
        # priority task already took it...
        # We run the things!
        for pri, rt in run_queue.items():
            print("RUN: task {} with eq: {}".format(rt[0].name, rt[1]))
            rt[0].take_action(rt[1])
