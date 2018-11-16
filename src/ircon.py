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

import db.EqFetch as eqfetch
import schedule.Scheduler as shd
import remote.Controller as rmc

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


eqfetch.load_all()
ventRetail = eqfetch.get("vent", "RETROOF")

vt25 = VentToPercent()
vt25.set_vent(ventRetail)
vt25.set_target(25)

shd.add_sequential(vt25)

shd.print_active_commands()

sThread = Thread(target=scheduler_loop)
sThread.start()

#time.sleep(20)

vt50 = VentToPercent()
vt50.set_vent(ventRetail)
vt50.set_target(-1)
shd.add_sequential(vt50)

cThread = Thread(target=controller_loop)
cThread.start()

#time.sleep(2.00)

dtp = DriveToPoint()
#shd.add_sequential(dtp)
