#!/usr/bin/python3

import time
import db.EqFetch as eqfetch
import rest.RestServer as rs
import schedule.Scheduler as shd
import schedule.TaskRunner as tr
import remote.Controller as rmc

from threading import Thread

print('starting')


def scheduler_loop():
    while True:
        shd.execute()
        time.sleep(0.10)


def task_loop():
    tr.load_tasks()
    while True:
        tr.execute()
        time.sleep(30)


# We'll let the controller loop stop the scheduler, insert commands, etc.
# It'll have a wide berth in what it can do instead of making the scheduler
# figure that out.  This lets us load up a remote UI with a lot of control.
def controller_loop():
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

    controller_thread = Thread(target=controller_loop)
    controller_thread.start()

    rest_thread = Thread(target=rest_loop)
    rest_thread.start()


eqfetch.load_all()
start_threads()
