from .BaseCommand import BaseCommand
from subsystem.Solenoid import Solenoid 

class WaterOn(BaseCommand):
	is_finished = False
	sol = Solenoid(2)

	def execute(self):
		self.sol.setOn()
		self.is_finished = True

	def isFinished(self):
		return self.is_finished

	def end(self):
		is_finished = False
