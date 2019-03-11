import db.EqFetch as eqfetch
from .BaseSubsystem import BaseSubsystem


class TempGroup(BaseSubsystem):

    group_contain = ['TEMP01']

    def __init__(self, long_name, short_name):
        self.long_name = long_name
        self.short_name = short_name

    def print_config(self):
        print("long name:", self.long_name)
        print("short name:", self.short_name)
        print("contains:", self.group_contains)

    def export_dict(self):
        data = {}
        data['long_name'] = self.long_name
        data['current_temp'] = self.get_temp()
        data['contains'] = self.group_contains

    def print_status(self):
        print(self.get_status())

    def get_status(self):
        return(self.short_name + " currently: " +
               str(round(self.get_temp(), 1)))

    def get_temp(self):
        total_temp = 0
        total_samples = 0
        for t in self.group_contains:
            temp_sens = eqfetch.get_vent(t)
            temp = temp_sens.get_temp()
            if temp is not None:
                total_temp += temp
                total_samples += 1

        avg_temp = total_temp / total_samples
        return avg_temp
