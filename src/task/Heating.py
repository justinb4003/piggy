from .BaseTask import BaseTask
from .TaskUnconfiguredError import TaskUnconfiguredError
import db.EqFetch as eqfetch


class Heating(BaseTask):

    prop_map = {}
    prop_map['heaters'] = eqfetch.get_heater
    prop_map['temp_sensor'] = eqfetch.get_temp
    prop_map['on_at'] = int
    prop_map['off_at'] = int

    # I'm going to need to define the madlib syntax someday soon, for now
    # it'll just grow randomly. A + after the type indicates a list is
    # desired.
    def get_madlib(self):
        return "Turn [Heater+:heaters] on at [int:on_at] and then " \
               "[int:off_at] according to [Temp:temp_sensor]."

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

        if temp is None:
            return False, None

        if temp <= self.on_at:
            for h in self.heaters:
                if h.is_on is False:
                    print("We want to turn heat {} on.".format(h.short_name))
                    ret_val = True
                    eq_wanted.append(h.short_name)
                    if doit and h.short_name in eq_cleared:
                        print("And we're trying to turn it on now.")
                        h.set_on()
                else:
                    # Heat is already on... no action needed.
                    pass

        if temp >= self.off_at:
            for h in self.heaters:
                if h.is_on is True:
                    print("We want to turn heat {} off.".format(h.short_name))
                    ret_val = True
                    eq_wanted.append(h.short_name)
                    if doit and h.short_name in eq_cleared:
                        print("And we're trying to turn it off now.")
                        h.set_off()
                else:
                    # Heat is already off... no action needed.
                    pass

        return ret_val, eq_wanted
