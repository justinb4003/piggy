#!/usr/bin/python3

from .BaseSubsystem import BaseSubsystem

class Heater(BaseSubsystem):
	def __init__(self, long_name, short_name, on_pin):
		self.long_name = long_name
		self.short_name = short_name
		self.on_pin = on_pin
		self.is_on = False

	def print_config(self):
		print("long_name:", self.long_name)
		print("short_name:", self.short_name)
		print("on_pin:", self.on_pin)

	def print_status(self):
		print(self.get_status())

	def get_status(self):
		lbl = "ON"
		if self.is_on == False:
			lbl = "OFF"
		return(self.short_name + " is " + lbl)
