from abc import ABC, abstractmethod
class BaseSubsystem(ABC):

	def __init__(self):
		pass

	@abstractmethod
	def to_json(self):
		pass

	@abstractmethod
	def get_status(self):
		pass

	@abstractmethod
	def print_status(self):
		pass
