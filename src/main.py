#!/usr/bin/python3

import time
import db.EqFetch as eqfetch
import rest.RestServer as rs
import schedule.Scheduler as shd
import schedule.TaskRunner as tr
import schedule.SensorTickle as tickler
import remote.Controller as rmc

from threading import Thread

print('starting')


def scheduler_loop():
    """
    The sheduler loop runs Commands that interface with hardware.
    Anything that would require controlling equipment for a period of
    time should issue a Command that can go into the scheduler.
    """
    while True:
        tickler.execute()
        shd.execute()
        time.sleep(0.10)


def task_loop():
    """
    Tasks figure out how to manipulate the equipment to achieve a goal.
    So, 'Heating' can be a task that just runs heater(s), A 'Cooling' task
    can run roof vents or side vents.  A 'Shading' task could control a heat
    curtain for shade, etc.

    This is what is going to make this project very flexible.  No task will
    actually be required by the system.  You could run it without any loaded
    at all but nothing would happen.  Users will be able to remove factory
    installed tasks entirely from the disk and if they want upload their own
    custom ones.  This way instead of having configuration options that your
    team has to remember you don't use, or remember not to turn on some
    features, you can simply remove them entirely.

    TODO: Create a configuration interface for tasks so you can configure
    them via a UI 'mad-lib' style.  Ie: When [temp_sensor] is over [num] deg
    activate [heater].
    """
    tr.load_tasks()
    while True:
        tr.execute()
        # 5 second sleep is WAY too fast for real life but nice for
        # testing.
        time.sleep(60)


def sensor_loop():
    """
    We're going to force a refresh on our sensors via a schedule instead of
    trying to do the I/O when something queries it.
    For now it's just a really simple delay loop and it'll bang through
    every sensor.  In the future this could get far more complex.
    """
    while True:
        tickler.execute()
        time.sleep(1)


# We'll let the controller loop stop the scheduler, insert commands, etc.
# It'll have a wide berth in what it can do instead of making the scheduler
# figure that out.  This lets us load up a remote UI with a lot of control.
def controller_loop():
    """
    Yeah haven't really done much with this yet.
    """
    rmc.init()
    while True:
        raw_command = rmc.listenForCommand()
        print("got command:",  str(raw_command))


def rest_loop():
    """Loop to start up a REST server that kicks back JSON status data"""
    rs.serve_forever()


def start_threads():
    scheduler_thread = Thread(target=scheduler_loop)
    scheduler_thread.start()

    task_thread = Thread(target=task_loop)
    task_thread.start()

    sensor_thread = Thread(target=sensor_loop)
    sensor_thread.start()

    controller_thread = Thread(target=controller_loop)
    controller_thread.start()

    rest_thread = Thread(target=rest_loop)
    rest_thread.start()


# Load all equipment from database
eqfetch.load_all()

# Bang on every sensor in the system once before we get going.  That'll
# let us load up default or initial values and we're also forcing all of
# that code to execute immediately on start.  Trap any errors and deal with
# them.
tickler.execute()

# Fire up all of our worker threads
start_threads()
