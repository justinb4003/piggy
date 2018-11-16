#!/usr/bin/python3

class Solenoid:
	openStatus = False
	outpin = -1

	def __init__(self, outpin):
		self.outpin = outpin

	def printConfig(self):
		print("outpin:", self.outpin)
		print("openStatus:", self.openStatus)

	def setOn(self):
		self.openStatus = True
		self.setStatus()

	def setOff(self):
		self.openStatus = False
		self.setStatus()

	def getStatus():
		return self.openStatus

	def setStatus(self):
		print("solenoid: ", self.outpin, " status:", self.openStatus)
		# Do the actual I/O here
		pass
