#!/usr/bin/python3

import json
import db.EqFetch as eqfetch
from http.server import HTTPServer, BaseHTTPRequestHandler



class RESTHTTPRequestHandler(BaseHTTPRequestHandler):
	def log_message(self, *args):
		pass # ignore logging anything to the screen for hits.

	def do_GET(self):
		self.send_response(200)
		self.end_headers()
		data = {}

		data['status'] = 'online'
		data['vents'] = {}
		data['heaters'] = {}
		data['temps'] = {}
		data['humiditys'] = {}

		for id, vent in eqfetch.get_vents().items():
			data['vents'][id] = vent.__dict__

		for id, heater in eqfetch.get_heaters().items():
			data['heaters'][id] = heater.__dict__

		for id, temp in eqfetch.get_temps().items():
			data['temps'][id] = temp.__dict__

		for id, humidity in eqfetch.get_humiditys().items():
			data['humiditys'][id] = humidity.__dict__

		self.wfile.write(bytes(json.dumps(data, sort_keys=True, indent=4), 'utf-8'))

def serve_forever():
	print("starting REST server...")
	httpd = HTTPServer(('0.0.0.0', 9999), RESTHTTPRequestHandler)
	print("probably on...")
	httpd.serve_forever()

