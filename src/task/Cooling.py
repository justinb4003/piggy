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
        d['name'] = self.name
        d['type'] = type(self).__name__
        d['setpoint'] = self.setpoint
        d['on_offset'] = self.on_offset
        d['off_offset'] = self.off_offset
        d['crack'] = self.crack
        d['step]'] = self.step
        d['want_action'] = self.want_action()
        return d

    def export_json_config(self):
        pass

    def import_json_config(self):
        pass

    def _action(self, doit):
        ret_val = False
        temp = self.temp_sensor.get_temp()
        temp_on = self.setpoint + self.on_offset
        temp_off = self.setpoint + self.off_offset
        print("COOLING________")
        print("setpoint: " + str(self.setpoint))
        print("on offset: " + str(self.on_offset))
        print("off offset: " + str(self.off_offset))
        print("temp: " + str(temp))
        print("temp_on:" + str(temp_on))
        print("temp_off:" + str(temp_off))
        print("vent1 is currently: " + str(self.vent1.get_percent()))

        vent_is_open = False
        if (self.vent1.get_percent() >= 0.00):
            vent_is_open = True

        if temp <= temp_off:
            print("temp <= temp_off")
            # If we're below the off temp for cooling then we try and move
            # the vents to -1.00% anyway.
            ret_val = True
            if doit:
                vtp = VentToPercent()
                vtp.set_vent(self.vent1)
                vtp.set_target(-1.00)
                shd.add_sequential(vtp)
            return  # Nothing else gets evaluated.  Vents are slamming closed.

        if temp >= temp_on and vent_is_open is False:
            print("temp >= temp_on and vent_is_open is False")
            # we're just opening the vents from a closed position.
            ret_val = True
            if doit:
                vtp = VentToPercent()
                vtp.set_vent(self.ven1)
                vtp.set_target(self.crack)
                shd.add_sequential(vtp)

        if vent_is_open and temp > self.setpoint:
            print("vent_is_open and temp > self.setpoint")
            ret_val = True
            if doit:
                vtp = VentToPercent()
                vtp.set_vent(self.vent1)
                vtp.set_target(self.vent1.get_percent() + self.step)
                shd.add_sequential(vtp)

        if vent_is_open and temp < self.setpoint:
            print("vent_is_open and temp < self.setpoint")
            ret_val = True
            if doit:
                vtp = VentToPercent()
                vtp.set_vent(self.vent1)
                vtp.set_target(self.vent1.get_percent() - self.step)
                shd.add_sequential(vtp)

        return ret_val
