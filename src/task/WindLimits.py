import db.EqFetch as eqfetch
import schedule.Scheduler as shd

from .BaseTask import BaseTask
from .TaskUnconfiguredError import TaskUnconfiguredError
from command.VentToPercent import VentToPercent


class WindLimits(BaseTask):

    """
    wind = eqfetch.get_wind_sensor("WIND")
    vent1 = eqfetch.get_vent("RETROOF")
    vent2 = eqfetch.get_vent("PRODROOF1")

    # Keeping it simple for now with just speed.  We'll get to direction
    # in a bit.
    max_wind = 15
    """

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
        self.name = str(valmap['name'])
        self.priority = int(valmap['priority'])
        self.vent1 = eqfetch.get_vent(valmap['vent1'])
        self.vent2 = eqfetch.get_vent(valmap['vent2'])
        self.wind = eqfetch.get_wind_sensor(valmap['wind_sensor'])
        self.max_wind = int(valmap['max_wind'])
        self.configured = True

    def export_as_dict(self):
        d = {}
        d['name'] = self.name
        d['priority'] = self.priority
        d['vent1'] = self.vent1
        d['vent2'] = self.vent2
        d['wind'] = self.wind
        d['max_wind'] = self.max_wind
        return d

    def export_json_config(self):
        pass

    def import_json_config(self):
        pass

    def _action(self, doit, eq_cleared):
        if self.configured is False:
            raise TaskUnconfiguredError()
        ret_val = False
        eq_wanted = []

        (wind_speed, wind_compass) = self.wind.get_wind()
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
