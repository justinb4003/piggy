import db.EqFetch as eqfetch
import schedule.Scheduler as shd

from .BaseTask import BaseTask
from .TaskUnconfiguredError import TaskUnconfiguredError
from command.CurtainToPercent import CurtainToPercent


class Shading(BaseTask):

    """
    temp_sensor = eqfetch.get_temp("TEMP01")
    sun_sensor = eqfetch.get_sun_sensor("SUN")
    curtain1 = eqfetch.get_curtain("RETSHADE")

    step = 10
    max_shade = 50
    on_at = 90
    off_at = 75
    """

    # Not even sure why I bother with step on this one. Might be an artifact
    # rather than a good idea.
    step = 10

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

    def get_madlib(self):
        return """Pull [Curtain:curtain1] to cool when [Temp:temp_sensor]
    is over [int:on_at] degees, up to [int:max_shade]%. Pull curtain back
    if temperature drops below [int:off_at]"""

    def import_by_dict(self, valmap):
        self.name = str(valmap['name'])
        self.priority = int(valmap['priority'])
        self.curtain1 = eqfetch.get_curtain(valmap['curtain1'])
        self.temp_sensor = eqfetch.get_temp(valmap['temp_sensor'])
        self.on_at = int(valmap['on_at'])
        self.off_at = int(valmap['off_at'])
        self.max_shade = int(valmap['max_shade'])
        self.configured = True

    def export_as_dict(self):
        d = {}
        d['name'] = self.name
        d['priority'] = self.priority
        d['curtain1'] = self.curtain1
        d['temp_sensor'] = self.temp_sensor
        d['on_at'] = self.on_at
        d['off_at'] = self.off_at
        d['max_shade'] = self.max_shade
        return d

    def _action(self, doit, eq_cleared):
        if self.configured is False:
            raise TaskUnconfiguredError()
        ret_val = False
        temp = self.temp_sensor.get_temp()
        pct = self.curtain1.get_percent()
        curtain = self.curtain1
        eq_wanted = []
        """
        print("SHADING:")
        print("on at: " + str(self.on_at))
        print("off at: " + str(self.off_at))
        print("temp: " + str(temp))
        print("curtain1 is currently: " + str(pct))
        """

        new_pct = pct
        if temp >= self.on_at:
            # For now keep cranking it closed until we max out.
            new_pct += self.step
        if temp <= self.off_at:
            # If our temp dropped below the off point we open it back up.
            new_pct = 0

        if new_pct > self.max_shade:
            new_pct = self.max_shade

        # If we can't move don't bother trying to change it.
        if curtain.can_move() is False:
            new_pct = pct

        if new_pct != pct:
            ret_val = True
            eq_wanted.append(self.curtain1.short_name)
            if doit and self.curtain1.short_name in eq_cleared:
                print("Setting shade curtain to new "
                      "percent: {}".format(str(new_pct)))
                ctp = CurtainToPercent()
                ctp.set_curtain(curtain)
                ctp.set_target(new_pct)
                shd.add_sequential(ctp)

        return ret_val, eq_wanted
