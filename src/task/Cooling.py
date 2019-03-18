import db.EqFetch as eqfetch
import schedule.Scheduler as shd

from .BaseTask import BaseTask
from .TaskUnconfiguredError import TaskUnconfiguredError
from command.VentToPercent import VentToPercent


class Cooling(BaseTask):

    prop_map = {}
    prop_map['vents'] = eqfetch.get_vent
    prop_map['temp_sensor'] = eqfetch.get_temp
    prop_map['on_at'] = int
    prop_map['off_at'] = int
    prop_map['crack'] = int
    prop_map['step'] = int

    def get_madlib(self):
        return("Begin opening [Vent+:vents] at [int:on_at] and then "
               "[int:off_at] according to [Temp:temp_sensor].  Vents will "
               "open first to [int:crack]% and then open [int:step]% after "
               "that.  I also need to explain/configure delay.")

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

        for v in self.vents:
            pct = v.get_percent()
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
            # It might be nice if there was an official contract for whether or
            # not a subsystem can take a command to it.
            #
            # I don't think the rejection of commands should be left to the
            # scheduler right now.  Leaving it at the task level allows any
            # task to take priority over the rest of the system.  That sounds
            # dangerous but ultimately I want the tasks to be simple and easy
            # to understand.  That'll make complex programming tasks easier to
            # implement.  I hope.  It could also end up a nightmare.  We'll
            # see.

            if v.can_move() is False:
                new_pct = pct

            if new_pct != pct:
                # Round it off so we're not hitting a goofy target like
                # 11.38282
                new_pct = round(new_pct, 0)
                ret_val = True
                eq_wanted.append(v.short_name)
                if doit is True and v.short_name in eq_cleared:
                    print("Setting vents to new percent: {}"
                          "".format(str(new_pct)))
                    vtp = VentToPercent()
                    vtp.set_vent(v)
                    vtp.set_target(new_pct)
                    shd.add_sequential(vtp)

        return ret_val, eq_wanted
