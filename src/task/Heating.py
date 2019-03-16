from .BaseTask import BaseTask
from .TaskUnconfiguredError import TaskUnconfiguredError
import db.EqFetch as eqfetch


class Heating(BaseTask):

    """
    temp_sensor = eqfetch.get_temp("TEMP01")
    heat1 = eqfetch.get_heater("HEAT01")

    on_at = 68
    off_at = 72
    """

    def __init__(self):
        self.configured = False

    def get_priority(self):
        return self.priority

    def set_priority(self, val):
        self.priority = val

    def get_madlib(self):
        return "Turn [Heater:heat1] on at [int:on_at] and then [int:off_at] " \
                "according to [Temp:temp_sensor]."

    def import_by_dict(self, valmap):
        self.name = str(valmap['name'])
        self.priority = int(valmap['priority'])
        self.heat1 = eqfetch.get_heater(valmap['heat1'])
        self.temp_sensor = eqfetch.get_temp(valmap['temp_sensor'])
        self.on_at = int(valmap['on_at'])
        self.off_at = int(valmap['off_at'])
        self.configured = True

    def export_as_dict(self):
        d = {}
        d['name'] = self.name
        d['priority'] = self.priority
        d['heat1'] = self.heat1
        d['temp_sensor'] = self.temp_sensor
        d['on_at'] = self.on_at
        d['off_at'] = self.off_at
        return d

    def take_action(self, eq_cleared):
        return self._action(True, eq_cleared)

    def want_action(self):
        return self._action(False, None)

    def _action(self, doit, eq_cleared):
        if self.configured is False:
            raise TaskUnconfiguredError
        ret_val = False
        eq_wanted = []
        temp = self.temp_sensor.get_temp()
        status = self.heat1.is_on
        # Some ugly debug code below
        print("HEATING task for {} using {} is:".format("HEAT01", "TEMP01"))
        print("... on at {} off at {} "
              "currently {} deg status: {}".format(self.on_at,
                                                   self.off_at,
                                                   temp, status))
        """
        print("temp: " + str(temp))
        print("heat1 on at: " + str(self.on_at))
        print("heat1 off at: " + str(self.off_at))
        print("heat1 is currently: " + str(self.heat1.is_on))
        """

        if (temp <= self.on_at and status is False):
            print("We want to turn heat on.")
            ret_val = True
            eq_wanted.append(self.heat1.short_name)
            if doit and self.heat1.short_name in eq_cleared:
                print("And we're trying to turn it on now.")
                self.heat1.set_on()

        if (temp >= self.off_at and status is True):
            print("We want to turn heat off.")
            ret_val = True
            eq_wanted.append(self.heat1.short_name)
            if doit and self.heat1.short_name in eq_cleared:
                print("And we're trying to turn it off now.")
                self.heat1.set_off()

        return ret_val, eq_wanted
