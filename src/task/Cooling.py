import db.EqFetch as eqfetch
import schedule.Scheduler as shd

from .BaseTask import BaseTask
from command.VentToPercent import VentToPercent


class Cooling(BaseTask):

    temp_sensor = eqfetch.get_temp("TEMP01")
    vent1 = eqfetch.get_vent("RETROOF")

    setpoint = 80
    crack = 8
    step = 3
    on_offset = 3
    off_offset = 0
    priority = 0

    def __init__(self, name, priority):
        self.name = name
        self.priority = priority

    def take_action(self):
        return self._action(True)

    def want_action(self):
        return self._action(False)

    def get_priority(self):
        return self.priority

    def set_priority(self, val):
        self.priority = val

    def export_dict(self):
        d = {}
        d['setpoint'] = self.setpoint
        d['on_offset'] = self.on_offset
        d['off_offset'] = self.off_offset
        d['crack'] = self.crack
        d['step]'] = self.step
        return d

    def export_json_config(self):
        pass

    def import_json_config(self):
        pass

    def _action(self, doit):
        ret_val = False
        temp = self.temp_sensor.get_temp()
        offset = temp - self.setpoint
        print("COOLING________")
        print("temp: " + str(temp))
        print("setpoint: " + str(self.setpoint))
        print("offset: " + str(offset))
        print("on offset: " + str(self.on_offset))
        print("off offset: " + str(self.off_offset))
        print("vent1 is currently: " + str(self.vent1.get_percent()))

        if offset < self.on_offset and self.vent1.can_move():
            ret_val = True  # we want to move!
            if self.vent1.get_percent() == 0.00:
                new_percent = self.crack
            else:
                new_percent = self.vent1.get_percent() + self.step

            if doit:
                print("Setting vent to: {0:0.0f}".format(new_percent))
                vtp = VentToPercent()
                vtp.set_vent(self.vent1)
                vtp.set_target(new_percent)
                shd.add_sequential(vtp)
        return ret_val
