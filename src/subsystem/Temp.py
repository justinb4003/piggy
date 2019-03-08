#!/usr/bin/python3

import json
import requests
import aiohttp

from .BaseSubsystem import BaseSubsystem
from .BaseSensor import BaseSensor


class Temp(BaseSubsystem, BaseSensor):

    current_temp = None

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
        data['current_temp'] = self.get_temp()

    def print_status(self):
        print(self.get_status())

    def get_status(self):
        return(self.short_name + " currently: " +
               str(round(self.get_temp(), 1)))

    async def _arefresh_value(self):
        async with aiohttp.ClientSession() as sess:
            async with sess.get(self.io_uri) as r:
                body = await r.text()
                data = json.loads(body)
                self.current_temp = data['temp']

    def _refresh_value(self):
        # print("getting temp from url: " + self.io_uri)
        try:
            r = requests.get(self.io_uri)
            data = json.loads(r.content.decode('utf-8'))
            # print("return data: " + str(data))
            self.current_temp = data['temp']
        except requests.exceptions.ConnectionError:
            self.current_temp = None
        return self.current_temp

    def get_temp(self):
        return self.current_temp
