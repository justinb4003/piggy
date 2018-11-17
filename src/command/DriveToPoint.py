from .BaseCommand import BaseCommand
from subsystem.DriveTrain import DriveTrain


class DriveToPoint(BaseCommand):
	dt = DriveTrain(3)
	is_finished = False
	counter = 0

	def execute(self):
		self.dt.setPower(0.50)
		self.counter += 1
		if self.counter > 5:
			self.is_finished = True

	def is_finished(self):
		return self.is_finished

	def end(self):
		self.dt.setPower(0.00)
		self.is_finished = False
		self.counter = 0
