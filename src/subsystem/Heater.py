#!/usr/bin/python3

from .BaseSubsystem import BaseSubsystem


class Heater(BaseSubsystem):
    def __init__(self, long_name, short_name, on_pin):
        self.long_name = long_name
        self.short_name = short_name
        self.on_pin = on_pin
        self.is_on = False
        self.on_offset = -2
        self.off_offset = 0

    def print_config(self):
        print("long_name:", self.long_name)
        print("short_name:", self.short_name)
        print("on_pin:", self.on_pin)

    def export_dict(self):
        data = {}
        data['long_name'] = self.long_name
        data['is_on'] = self.is_on
        data['on_offset'] = self.on_offset
        data['off_offset'] = self.off_offset
        return data

    def print_status(self):
        print(self.get_status())

    def get_status(self):
        lbl = "ON"
        if self.is_on is False:
            lbl = "OFF"
            return(self.short_name + " is " + lbl)

    def set_on(self):
        self.is_on = True
        # do the io
        pass

    def set_off(self):
        self.is_on = False
        # do the io
        pass
