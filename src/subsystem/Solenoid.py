#!/usr/bin/python3

from .BaseSubsystem import BaseSubsystem

class Solenoid(BaseSubsystem):
	open_status = False
	outpin = -1

	def __init__(self, outpin):
		self.outpin = outpin

	def print_config(self):
		print("outpin:", self.outpin)
		print("open_status:", self.open_status)

	def set_on(self):
		self.open_status = True
		self.setStatus()

	def set_off(self):
		self.open_status = False
		self.setStatus()

	def get_status(self):
		return self.open_status

	def print_status(self):
		print(self.get_status())

	def set_status(self):
		print("solenoid: ", self.outpin, " status:", self.open_status)
		# Do the actual I/O here
		pass
