from abc import ABC, abstractmethod

class BaseTask(ABC):

	def __init__(self):
		pass

	@abstractmethod
	def take_action(self):
		pass

	@abstractmethod
	def want_action(self):
		pass

	@abstractmethod
	def export_dict(self):
		pass
