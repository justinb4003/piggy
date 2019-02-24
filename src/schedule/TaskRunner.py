from threading import Lock
from task.Heating import Heating
from task.Cooling import Cooling

task_lock = Lock()
task_list = []


def export_dict():
    """
    Export running tasks to a dict so we can JSON format them
    """
    pass


def create_obj(obj_name):
    classes = {
        'Heating': Heating,
        'Cooling': Cooling
    }
    return classes[obj_name]


def load_tasks():
    """
    Pull tasks from DB and set them up to run. We want to be able to hit
    this on the fly with a running system, hence the locking.
    """
    with task_lock:
        task_list.clear()
        task = create_obj("Heating")('Basic Heating', 1)
        task_list.append(task)
        """
        task2 = create_obj("Cooling")('Basic Cooling', 8)
        task_list.append(task2)
        """


def execute():
    """
    Loop through the tasks and figure out what we need to
    actually do on this iteration.
    Interval that this is hit at will be configurable, but should be
    something like 30-60 seconds.
    """
    with task_lock:
        for task in task_list:
            # want = task.want_action()
            # print("Does {} want to run? {}".format(task.name, want))
            # TODO: Resolve conflicts between tasks that wants to utilize
            # the same equipment at the same time.
            # For now we'll just let every action do it's thing immediately
            task.take_action()
    pass
