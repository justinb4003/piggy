# vim: ai ts=4 sw=4 expandtab softtabstop=4 filetype=python

# OK, so a Curtain and a Vent are basically identical.
# I really don't even know if we need a different class for this.
# Odds are I'll find something differnt about it though.

import time
from .BaseSubsystem import BaseSubsystem


class Curtain(BaseSubsystem):
    def __init__(self, long_name, short_name, open_io_url, close_io_url,
                 stroke_seconds):
        self.long_name = long_name
        self.short_name = short_name
        self.open_io_url = open_io_url
        self.close_io_url = close_io_url
        self.stroke = stroke_seconds
        self.curr_pct = 0
        self.is_closing = False
        self.is_opening = False
        self.start_runtime = 0
        self.last_moved_at = 0

    def print_config(self):
        print("long_name:", self.long_name)
        print("short_name:", self.short_name)
        print("open_io_url:", self.open_io_url)
        print("close_io_url:", self.close_io_url)

    def export_dict(self):
        data = {}
        data['long_name'] = self.long_name
        data['current_percent'] = self.get_percent()
        data['is_closing'] = self.is_closing
        data['is_opening'] = self.is_opening
        return data

    def print_status(self):
        print(self.get_status())

    def get_status(self):
        return(self.short_name + " percent open:",
               round(self.get_percent(), 1))

    def set_close(self):
        if (self.can_move()):
            self.start_runtime = time.time()
            self.is_closing = True
            print("{} set to closing.".format(self.short_name))
            # do the actual io
            pass

    def set_open(self):
        if (self.can_move()):
            self.start_runtime = time.time()
            self.is_opening = True
            print("{} set to opening.".format(self.short_name))
            # do the actual io
            pass

    def get_percent(self):
        now = time.time()
        delta = now - self.start_runtime
        frac = (delta / self.stroke)
        new_pct = self.curr_pct

        if (self.is_closing):
            new_pct = self.curr_pct - frac*100.0
        if (self.is_opening):
            new_pct = self.curr_pct + frac*100.0

        return new_pct

    def stop(self):
        self.curr_pct = self.get_percent()

        # fix percent if it's over a limit
        if self.curr_pct < 0:
            self.curr_pct = 0
        if self.curr_pct > 100:
            self.curr_pct = 100

        print("STOPPING CURTAIN")

        if (self.is_closing and self.is_opening):
            print("Somehow this curtain was both opening and " +
                  "closing which is bad.")

        self.is_closing = False
        self.is_opening = False
        self.start_runtime = 0
        self.last_moved_at = time.time()
        # do the actual io
        pass

    def can_move(self):
        # Internal rules to see if the curtain can move.
        # for now it's just the timeout.  30 seconds between movements.
        now = time.time()
        if self.is_closing:
            print("no: closing ", end='', flush=True)
            return False
        if self.is_opening:
            print("no: opening ", end='', flush=True)
            return False
        if now - self.last_moved_at < 30:
            rem = 30 - (now - self.last_moved_at)
            print("no: {}s left ".format(rem))
            return False
        return True  # yay we made it!
