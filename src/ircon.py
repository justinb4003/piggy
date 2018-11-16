#!/usr/bin/python3

print('starting')

from threading import Thread
import time

from command.DriveToPoint import DriveToPoint
from command.WaterOn import WaterOn

import schedule.Scheduler as shd
import remote.Controller as rmc

def scheduler_loop():
	while True:
		shd.execute()
		time.sleep(0.10)

def controller_loop():
	rmc.init()
	while True:
		print("got command:",  str(rmc.listenForCommand()))

dtp = DriveToPoint()
won = WaterOn()

shd.addSequential(dtp)
shd.addSequential(won)

shd.printActiveCommands()

sThread = Thread(target=scheduler_loop)
sThread.start()

cThread = Thread(target=controller_loop)
cThread.start()

time.sleep(2.00)

dtp = DriveToPoint()
#shd.addSequential(dtp)
