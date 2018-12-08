#!/usr/bin/python3

print('starting')

DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "nothing"
DB_SCHM = "ircon"

import pymysql

from threading import Thread
import time

from command.VentToPercent import VentToPercent
from command.DriveToPoint import DriveToPoint

from http.server import HTTPServer, BaseHTTPRequestHandler

import db.EqFetch as eqfetch
import rest.RestServer as rs
import schedule.Scheduler as shd
import remote.Controller as rmc
import monitor.Monitor as mon

def scheduler_loop():
	while True:
		shd.execute()
		time.sleep(0.10)

# We'll let the controller loop stop the scheduler, insert commands, etc.
# It'll have a wide berth in what it can do instead of making the scheduler
# figure that out.  This lets us load up a remote UI with a lot of control.
def controller_loop():
	rmc.init()
	while True:
		raw_command = rmc.listenForCommand()
		print("got command:",  str(raw_command))


def monitor_loop():
	"""Something that runs constantly updating a display or maybe more.  Not sure yet"""
	while True:
		mon.execute()
		time.sleep(5.0)

def rest_loop():
	"""Loop to start up a REST server that kicks back JSON status data"""
	rs.serve_forever()

def start_threads():
	scheduler_thread = Thread(target=scheduler_loop)
	scheduler_thread.start()

	controller_thread = Thread(target=controller_loop)
	controller_thread.start()

	monitor_thread = Thread(target=monitor_loop)
	monitor_thread.start()

	rest_thread = Thread(target=rest_loop)
	rest_thread.start()


eqfetch.load_all()
start_threads()
