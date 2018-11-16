#!/usr/bin/python3

print('starting')

from threading import Thread
import time

from command.DriveToPoint import DriveToPoint
from command.WaterOn import WaterOn
from command.VentToPercent import VentToPercent

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

dtp = DriveToPoint()
won = WaterOn()
vt25 = VentToPercent()
vt25.setTarget(25)

shd.addSequential(dtp)
shd.addSequential(won)
shd.addSequential(vt25)

shd.printActiveCommands()

sThread = Thread(target=scheduler_loop)
sThread.start()

time.sleep(20)

vt50 = VentToPercent()
vt50.setTarget(-1)
shd.addSequential(vt50)

cThread = Thread(target=controller_loop)
cThread.start()

time.sleep(2.00)

dtp = DriveToPoint()
#shd.addSequential(dtp)
