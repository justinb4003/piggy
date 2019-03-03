from abc import ABC, abstractmethod


class BaseSensor(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def _refresh_value(self):
        pass
