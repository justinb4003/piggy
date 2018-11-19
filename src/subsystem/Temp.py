#!/usr/bin/python3

import json
import requests

from .BaseSubsystem import BaseSubsystem

class Temp(BaseSubsystem):
	def __init__(self, long_name, short_name, io_uri):
		self.long_name = long_name
		self.short_name = short_name
		self.io_uri = io_uri 

	def print_config(self):
		print("long name:", self.long_name)
		print("short name:", self.short_name)
		print("io_uri:", self.io_uri)

	def to_json(self):
		data = {}
		data['long_name'] = self.long_name
		data['current_temp'] = self.get_temp()

	def print_status(self):
		print(self.get_status())

	def get_status(self):
		return(self.short_name + " currently: " + str(round(self.get_temp(), 1)))

	# TODO: This needs some serious error handling.
	# Break it out into some shared function.
	def get_temp(self):
		#print("getting temp from url: " + self.io_uri)
		r = requests.get(self.io_uri)
		data = json.loads(r.content)
		#print("return data: " + str(data))
		return data['temp'] 
