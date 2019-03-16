import db.EqFetch as eqfetch
import schedule.Scheduler as shd

from .BaseTask import BaseTask
from .TaskUnconfiguredError import TaskUnconfiguredError
from command.VentToPercent import VentToPercent


class WindLimits(BaseTask):

    prop_map = {}
    prop_map['name'] = str
    prop_map['priority'] = int
    prop_map['vent1'] = eqfetch.get_vent
    prop_map['vent2'] = eqfetch.get_vent
    prop_map['wind_sensor'] = eqfetch.get_wind_sensor
    prop_map['max_wind'] = int

    def __init__(self):
        self.configured = False

    def take_action(self, eq_cleared):
        return self._action(True, eq_cleared)

    def want_action(self):
        return self._action(False, None)

    def get_priority(self):
        return self.priority

    def set_priority(self, val):
        self.priority = val

    def import_by_dict(self, valmap):
        super().import_by_dict(valmap)

    def export_as_dict(self):
        super().export_as_dict()

    def _action(self, doit, eq_cleared):
        if self.configured is False:
            raise TaskUnconfiguredError()
        ret_val = False
        eq_wanted = []

        (wind_speed, wind_compass) = self.wind_sensor.get_wind()
        print("Wind limits has {}mph max and current is {} mph"
              "".format(self.max_wind, wind_speed))

        if wind_speed >= self.max_wind:
            # Slam every vent shut...
            # Do _not_ test for can_move() ... don't care.
            ret_val = True

            for v in [self.vent1, self.vent2]:
                eq_wanted.append(v.short_name)
                print("Want to slam vent {} 'cuz wind.".format(v.short_name))
                if doit is True and v.short_name in eq_cleared:
                    print("Slamming vent {} due to winds {}mph from {}"
                          "".format(v.short_name, wind_speed, wind_compass))
                    vtp = VentToPercent()
                    vtp.set_vent(v)
                    vtp.set_target(-1)
                    shd.add_sequential(vtp)

        return ret_val, eq_wanted
