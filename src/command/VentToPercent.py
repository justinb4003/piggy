from .BaseCommand import BaseCommand
from subsystem.Vent import Vent 

class VentToPercent(BaseCommand):
	#vent = Vent("Roof vent", 2, 4, 30)

	def set_vent(self, vent):
		self.vent = vent

	def set_target(self, target):
		self.target_pct = target

	def execute(self):
		# There should probably be some ramping here but that'll
		# depend entirely on the controller.`
		if (self.vent.get_percent() < self.target_pct):
			self.vent.set_open()
		else:
			self.vent.set_close()

	def is_finished(self):
		if ( abs(self.vent.get_percent() - self.target_pct) < 0.5 ):
			return True
		return False

	def end(self):
		self.vent.stop()
		
	

