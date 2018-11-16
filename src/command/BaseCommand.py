from abc import ABC, abstractmethod
class BaseCommand(ABC):

	def __init__(self):
		pass

	@abstractmethod
	def execute(self):
		pass

	@abstractmethod
	def is_finished(self):
		pass

	@abstractmethod
	def end(self):
		pass
