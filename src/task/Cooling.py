import db.EqFetch as eqfetch
import schedule.Scheduler as shd

from .BaseTask import BaseTask
from .TaskUnconfiguredError import TaskUnconfiguredError
from command.VentToPercent import VentToPercent


class Cooling(BaseTask):

    """
    temp_sensor = eqfetch.get_temp("TEMP01")
    vent1 = eqfetch.get_vent("RETROOF")

    crack = 8
    step = 3
    on_at = 82
    off_at = 78
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
        self.temp_sensor = eqfetch.get_temp(valmap['temp_sensor'])
        self.on_at = int(valmap['on_at'])
        self.off_at = int(valmap['off_at'])
        self.crack = int(valmap['crack'])
        self.step = int(valmap['step'])
        self.configured = True

    def export_as_dict(self):
        d = {}
        d['name'] = self.name
        d['priority'] = self.priority
        d['vent1'] = self.vent1
        d['temp_sensor'] = self.temp_sensor
        d['on_at'] = self.on_at
        d['off_at'] = self.off_at
        d['crack'] = self.crack
        d['step]'] = self.step
        return d

    def _action(self, doit, eq_cleared):
        if self.configured is False:
            raise TaskUnconfiguredError
        ret_val = False
        eq_wanted = []
        temp = self.temp_sensor.get_temp()
        pct = self.vent1.get_percent()
        vent = self.vent1
        """
        print("COOLING:")
        print("on at: " + str(self.on_at))
        print("off at: " + str(self.off_at))
        print("temp: " + str(temp))
        print("vent1 is currently: " + str(pct))
        """

        if temp is None:
            return False, None

        new_pct = pct
        if temp >= self.on_at and pct <= 0:
            # If we need to open but it's the first move we only go the
            # 'crack' positon.
            new_pct = self.crack
        if temp >= self.on_at and pct > 0:
            # If we need to open but we're already partly open we just move
            # up another 'step'
            new_pct = pct + self.step

        """
        I'm going to stop doing this in the Cooling task. This is more of a
        safety check that belongs elsewhere.
        if temp <= self.off_at:
            # If our temp dropped below the off point we slam them shut
            # pronto.
            new_pct = -1
        """

        # THINK: Is this where we should be checking if a subsystem can
        # actually take a command?  I'm not sure who's job that should be.
        #
        # If you leave it up the task the worst that can happen is you have
        # actions queued up that may not really be necessary.  For instance
        # before this commit the vent would always be targeting one extra
        # 'step' ahead from where it could actually get.
        #
        # It might be nice if there was an official contract for whether
        # or not a subsystem can take a command to it.
        #
        # I don't think the rejection of commands should be left to the
        # scheduler right now.  Leaving it at the task level allows any
        # task to take priority over the rest of the system.  That sounds
        # dangerous but ultimately I want the tasks to be simple and easy
        # to understand.  That'll make complex programming tasks easier to
        # implement.  I hope.  It could also end up a nightmare.  We'll see.
        if vent.can_move() is False:
            new_pct = pct

        if new_pct != pct:
            # Round it off so we're not hitting a goofy target like 11.38282
            new_pct = round(new_pct, 0)
            ret_val = True
            eq_wanted.append(self.vent1.short_name)
            if doit is True and self.vent1.short_name in eq_cleared:
                print("Setting vents to new percent: {}".format(str(new_pct)))
                vtp = VentToPercent()
                vtp.set_vent(vent)
                vtp.set_target(new_pct)
                shd.add_sequential(vtp)

        return ret_val, eq_wanted
