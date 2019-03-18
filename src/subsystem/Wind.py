import json
import requests
import aiohttp

from .BaseSubsystem import BaseSubsystem


class Wind(BaseSubsystem):
    wind_speed = 0
    wind_compass = 'NW'

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
        data['short_name'] = self.short_name
        data['current_wind'] = self.get_wind()
        data['current_wind_speed'] = self.get_wind_speed()
        data['current_wind_compass'] = self.get_wind_compass()
        return data

    def print_status(self):
        print(self.get_status())

    def get_status(self):
        return "{} currently {}mph from {}".format(self.short_name,
                                                   self.get_wind_speed(),
                                                   self.get_wind_compass())

    def get_wind_speed(self):
        return self.wind_speed

    def get_wind_compass(self):
        return self.wind_compass

    async def _arefresh_value(self):
        async with aiohttp.ClientSession() as sess:
            async with sess.get(self.io_uri) as r:
                body = await r.text()
                data = json.loads(body)
                self.wind_speed = data['wind_speed']
                self.wind_compass = 'N'

    def _refresh_value(self):
        # print("getting wind from url: " + self.io_uri)
        try:
            r = requests.get(self.io_uri)
            data = json.loads(r.content.decode('utf-8'))
            # print("return data: " + str(data))
            self.wind_speed = data['wind_speed']
            self.wind_compass = 'N'
        except requests.exceptions.ConnectionError:
            self.wind_speed = None
            self.wind_compass = None

    def get_wind(self):
        return (self.wind_speed, self.wind_compass)
