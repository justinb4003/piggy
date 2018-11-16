#!/usr/bin/python3

# Ugh... gotta make sure I keep this all DT safe and what not.  
import time

class Vent:
	# why do I do this? C habit?
	name = ""
	openPin = -1
	closePin = -1
	curr_pct = 0

	def __init__(self, name, openPin, closePin, stroke):
		self.name = name
		self.openPin = openPin
		self.closePin = closePin
		self.curr_pct = 0
		self.stroke = stroke

		self.isClosing = False
		self.isOpening = False
		self.startRuntime = 0

	def printConfig(self):
		print("name:", self.name)
		print("openPin:", self.openPin)
		print("closePin:", self.closePin)
		print("Percent Open:", self.getPercent())

	def printStatus(self):
		print(self.name + " percent open:", self.getPercent())

	def setClose(self):
		# if we're already at -1 and want to go to -1 again then we want to
		# make sure we're really shut so reset back to 0 and let it close
		# for a bit.
		if (self.curr_pct < 0):
			self.curr_pct = 0

		if (self.isClosing == False):
			self.startRuntime = time.time()
			self.isClosing = True
		# do the actual io
		pass

	def setOpen(self):
		# if we're already at 101 and want to go to 101 again then we want to
		# make sure we're really open so reset back to 100 and let it open
		# for a bit.
		if (self.curr_pct > 100):
			self.curr_pct = 100 

		if (self.isOpening == False):
			self.startRuntime = time.time()
			self.isOpening = True
		# do the actual io
		pass

	def getPercent(self):
		now = time.time()
		delta = now - self.startRuntime
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

