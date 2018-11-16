from .BaseCommand import BaseCommand
from subsystem.Vent import Vent 

class VentToPercent(BaseCommand):
	vent = Vent(2, 4, 30)

	def setTarget(self, target):
		self.target_pct = target

	def execute(self):
		# holy shit this is bad... fix when not high
		if (self.vent.getPercent() < self.target_pct):
			self.vent.setOpen()
		else:
			self.vent.setClose()

	def isFinished(self):
		if ( abs(self.vent.getPercent() - self.target_pct) < 0.5 ):
			return True
		return False

	def end(self):
		self.vent.stop()
		
	

