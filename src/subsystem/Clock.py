import datetime

from .BaseSubsystem import BaseSubsystem
from .BaseSensor import BaseSensor


class Clock(BaseSubsystem, BaseSensor):

    clock_init = None
    clock_curr = None
    clock_mult = 1.0

    def __init__(self):
        self.clock_init = datetime.datetime.now()

    def _refresh_value(self):
        now = datetime.datetime.now()
        td = now - self.clock_init
        td *= self.clock_mult
        # print(td)
        self.clock_curr = td + self.clock_init

    def set_mult(self, mult):
        self.clock_mult = mult

    def get_status(self):
        return self.clock_curr

    def print_status(self):
        print(self.get_status())

    def export_dict(self):
        data = {}
        data['clock_init'] = self.clock_init
        data['clock_mult'] = self.clock_mult
        return data
