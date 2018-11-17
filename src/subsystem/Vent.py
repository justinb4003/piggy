#!/usr/bin/python3

# Ugh... gotta make sure I keep this all DT safe and what not.  
import time
from .BaseSubsystem import BaseSubsystem

class Vent(BaseSubsystem):
	def __init__(self, long_name, short_name, open_pin, close_pin, stroke):
		self.long_name = long_name
		self.short_name = short_name
		self.open_pin = open_pin
		self.close_pin = close_pin
		self.curr_pct = 0
		self.stroke = stroke
		print("init stroke: " + str(stroke))

		self.is_closing = False
		self.is_opening = False
		self.start_runtime = 0

	def print_config(self):
		print("name:", self.name)
		print("openPin:", self.open_pin)
		print("closePin:", self.close_pin)
		print("Percent Open:", self.get_percent())

	def print_status(self):
		print(self.get_status())

	def get_status(self):
		return(self.short_name + " percent open:", self.get_percent())

	def set_close(self):
		if (self.is_closing == False):
			self.start_runtime = time.time()
			self.is_closing = True
		# do the actual io
		pass

	def set_open(self):
		if (self.is_opening == False):
			self.start_runtime = time.time()
			self.is_opening = True
		# do the actual io
		pass

	def get_percent(self):
		now = time.time()
		delta = now - self.start_runtime
		frac = (delta / self.stroke) 
		new_pct = self.curr_pct

		if (self.is_closing):
			new_pct = self.curr_pct - frac*100.0
		if (self.is_opening):
			new_pct = self.curr_pct + frac*100.0

		return new_pct

	def stop(self):
		self.curr_pct = self.get_percent()

		# fix percent if it's over a limit
		if self.curr_pct < 0:
			self.curr_pct = 0
		if self.curr_pct > 100:
			self.curr_pct = 100

		print("STOPPING VENTS!")
		if (self.is_closing and self.is_opening):
			print("Somehow this vent was both opening and closing which is bad.")
		self.is_closing = False
		self.is_opening = False
		self.start_runtime = 0
		# do the actual io
		pass

