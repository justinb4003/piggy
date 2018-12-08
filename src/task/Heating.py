from .BaseTask import BaseTask
import db.EqFetch as eqfetch


class Heating(BaseTask):

    temp_sensor = eqfetch.get_temp("TEMP01")
    heat1 = eqfetch.get_heater("HEAT01")
    heat2 = eqfetch.get_heater("HEAT02")

    setpoint = 72
    on_offset = -4
    off_offset = 0

    def take_action(self):
        return self._action(True)

    def want_action(self):
        return self._action(False)

    def export_dict(self):
        d = {}
        d['setpoint'] = self.setpoint
        d['on_offset'] = self.on_offset
        d['off_offset'] = self.off_offset
        return d

    def _action(self, doit):
        ret_val = False
        temp = self.temp_sensor.get_temp()
        offset = temp - self.setpoint
        print("HEATING________")
        print("temp: " + str(temp))
        print("setpoint: " + str(self.setpoint))
        print("offset: " + str(offset))
        print("heat1 on offset: " + str(self.heat1.on_offset))
        print("heat1 off offset: " + str(self.heat1.off_offset))
        print("heat1 is currently: " + str(self.heat1.is_on))

        if (self.heat1.on_offset >= offset and self.heat1.is_on is False):
            ret_val = True
            if doit:
                self.heat1.set_on()
        if (self.heat1.off_offset <= offset and self.heat1.is_on is True):
            ret_val = True
            if doit:
                self.heat1.set_off()
        return ret_val
