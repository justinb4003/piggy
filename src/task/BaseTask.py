from abc import ABC, abstractmethod


class BaseTask(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def import_json_config(self, jsons):
        pass

    @abstractmethod
    def export_json_config(self):
        pass

    @abstractmethod
    def take_action(self):
        pass

    @abstractmethod
    def want_action(self):
        pass

    @abstractmethod
    def get_priority(self):
        pass

    @abstractmethod
    def export_dict(self):
        pass
