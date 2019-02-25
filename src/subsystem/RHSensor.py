#!/usr/bin/python3

import json
import requests
from .BaseSubsystem import BaseSubsystem


class RHSensor(BaseSubsystem):
    def __init__(self, long_name, short_name, io_uri):
        self.long_name = long_name
        self.short_name = short_name
        self.io_uri = io_uri

    def print_config(self):
        print("long name:", self.long_name)
        print("short name:", self.short_name)
        print("io_uri:", self.io_uri)

    def export_dict(self):
        data = {}
        data['long_name'] = self.long_name
        data['current_rh'] = self.get_rh()
        return data

    def print_status(self):
        print(self.get_status())

    def get_status(self):
        return(self.short_name + " currently: " + str(round(self.get_rh(), 1)))

    def get_rh(self):
        # print("getting humidity from url: " + self.io_uri)
        r = requests.get(self.io_uri)
        data = json.loads(r.content.decode('utf-8'))
        # print("return data: " + str(data))
        return data['humidity']
