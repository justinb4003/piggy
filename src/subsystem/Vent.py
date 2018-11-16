#!/usr/bin/python3

# Ugh... gotta make sure I keep this all DT safe and what not.  
import time

class Vent:
	# why do I do this? C habit?
	openPin = -1
	closePin = -1
	curr_pct = 0

	def __init__(self, openPin, closePin, stroke):
		self.openPin = openPin
		self.closePin = closePin
		self.curr_pct = 0
		self.stroke = stroke

		self.isClosing = False
		self.isOpening = False
		self.startRuntime = 0

	def printConfig(self):
		print("openPin:", self.openPin)
		print("closePin:", self.closePin)
		print("curr_pct:", self.curr_pct)

	def setClose(self):
		print("Closing vents. Currently at: " + str(self.getPercent()))
		if (self.isClosing == False):
			self.startRuntime = time.time()
			self.isClosing = True
		# do the actual io
		pass

	def setOpen(self):
		print("Opening vents. Currently at: " + str(self.getPercent()))
		if (self.isOpening == False):
			self.startRuntime = time.time()
			self.isOpening = True
		# do the actual io
		pass

	def getPercent(self):
		now = time.time()
		delta = now - self.startRuntime
		print("seconds runtime: " + str(delta))
		frac = (delta / self.stroke) 
		new_pct = self.curr_pct

		if (self.isClosing):
			new_pct = self.curr_pct - frac*100.0
		if (self.isOpening):
			new_pct = self.curr_pct + frac*100.0

#		if (new_pct < 0):
#			new_pct = 0
#
#		if (new_pct > 100):
#			new_pct = 100
		return new_pct

	def stop(self):
		self.curr_pct = self.getPercent()
		print("STOPPING VENTS!")
		if (self.isClosing and self.isOpening):
			print("Somehow this vent was both opening and closing which is bad.")
		self.isClosing = False
		self.isOpening = False
		self.startRuntime = 0
		# do the actual io
		pass

