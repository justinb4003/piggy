import json
import requests
from .BaseSubsystem import BaseSubsystem


class RHSensor(BaseSubsystem):
    rh = 0

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
        data['current_rh'] = self.rh
        return data

    def print_status(self):
        print(self.get_status())

    def get_status(self):
        return(self.short_name + " currently: " + str(round(self.rh, 1)))

    def _refresh_value(self):
        # print("getting humidity from url: " + self.io_uri)
        r = requests.get(self.io_uri)
        data = json.loads(r.content.decode('utf-8'))
        # print("return data: " + str(data))
        self.rh = data['humidity']

    def get_rh(self):
        return self.rh
