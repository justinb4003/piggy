from abc import ABC, abstractmethod
from .TaskUnconfiguredError import TaskUnconfiguredError


class BaseTask(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def get_priority(self):
        pass

    @abstractmethod
    def set_priority(self):
        pass

    @abstractmethod
    def export_as_dict(self):
        pass

    @abstractmethod
    def import_by_dict(self, valmap):
        pass

    # Accepts a tuple of equipment allowed the task is allowed to maninpulate.
    # If the list of cleared equipment is not everything the task wanted
    # it will be up to the task to decide if partially proceeding works.
    @abstractmethod
    def take_action(self, eq_cleared):
        pass

    # Returns true or false then a list of equipment the task needs to
    # manipulate to carry out the action
    @abstractmethod
    def want_action(self):
        pass
