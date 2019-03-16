import json
import inspect
import importlib
from threading import Lock
import db.TaskFetch as taskfetch

task_lock = Lock()
task_list = []


def export_dict():
    """
    Export running tasks to a dict so we can JSON format them
    """
    pass


def _create_obj(obj_name):
    mod = importlib.import_module("task.{}".format(obj_name))
    members = dict(inspect.getmembers(mod))
    return members[obj_name]()


def save_tasks():
    # TODO: Really need to look at how we lock this.
    with task_lock:
        taskfetch.save_tasks(task_list)


def add_task(task_type, name, pri, json_config):
    new_task = _create_obj(task_type)
    # name and priority are also in the dict.
    # weird duplication thing I was doing and I'm not sure which way I'll go.
    # new_task.set_name(name)
    # new_task.set_priority(pri)
    new_task.import_by_dict(json.loads(json_config))

    with task_lock:
        task_list.append(new_task)

    print("Created object of type {}".format(task_type))
    print("config: {}".format(json_config))


def load_tasks():
    """
    Pull tasks from DB and set them up to run. We want to be able to hit
    this on the fly with a running system, hence the locking.
    """
    with task_lock:
        task_list.clear()

    tconfig = taskfetch.get_tasks()
    for t in tconfig:
        task_type = t['task_type']
        task_name = t['task_name']
        priority = t['priority']
        json_config = t['json_config']
        add_task(task_type, task_name, priority, json_config)


def execute():
    """
    Loop through the tasks and figure out what we need to
    actually do on this iteration.
    Interval that this is hit at will be configurable, but should be
    something like 30-60 seconds.
    """
    with task_lock:
        run_queue = {}
        for task in sorted(task_list, key=lambda task: task.get_priority()):
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
