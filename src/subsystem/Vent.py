#!/usr/bin/python3

# Ugh... gotta make sure I keep this all DT safe and what not.  
import time
from .BaseSubsystem import BaseSubsystem

class Vent(BaseSubsystem):
	def __init__(self, long_name, short_name, openPin, closePin, stroke):
		self.long_name = long_name
		self.short_name = short_name
		self.openPin = openPin
		self.closePin = closePin
		self.curr_pct = 0
		self.stroke = stroke
		print("init stroke: " + str(stroke))

		self.is_closing = False
		self.is_opening = False
		self.start_runtime = 0

	def print_config(self):
		print("name:", self.name)
		print("openPin:", self.openPin)
		print("closePin:", self.closePin)
		print("Percent Open:", self.getPercent())

	def print_status(self):
		print(self.get_status())

	def get_status(self):
		return(self.short_name + " percent open:", self.getPercent())

	def set_close(self):
		# if we're already at -1 and want to go to -1 again then we want to
		# make sure we're really shut so reset back to 0 and let it close
		# for a bit.
		if (self.curr_pct < 0):
			self.curr_pct = 0

		if (self.is_closing == False):
			self.start_runtime = time.time()
			self.is_closing = True
		# do the actual io
		pass

	def set_open(self):
		# if we're already at 101 and want to go to 101 again then we want to
		# make sure we're really open so reset back to 100 and let it open
		# for a bit.
		if (self.curr_pct > 100):
			self.curr_pct = 100 

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

#		if (new_pct < 0):
#			new_pct = 0
#
#		if (new_pct > 100):
#			new_pct = 100
		return new_pct

	def stop(self):
		self.curr_pct = self.get_percent()
		print("STOPPING VENTS!")
		if (self.is_closing and self.is_opening):
			print("Somehow this vent was both opening and closing which is bad.")
		self.is_closing = False
		self.is_opening = False
		self.start_runtime = 0
		# do the actual io
		pass

