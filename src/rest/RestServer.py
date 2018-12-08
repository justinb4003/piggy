#!/usr/bin/python3

import json
import db.EqFetch as eqfetch
from http.server import HTTPServer, BaseHTTPRequestHandler


class RESTHTTPRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # ignore logging anything to the screen for hits.

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        data = {}

        data['status'] = 'online'
        data['equipment'] = {}
        _eq = data['equipment']
        _eq['vents'] = {}
        _eq['heaters'] = {}
        _eq['temps'] = {}
        _eq['humiditys'] = {}

        for id, vent in eqfetch.get_vents().items():
            _eq['vents'][id] = vent.export_dict()

        for id, heater in eqfetch.get_heaters().items():
            _eq['heaters'][id] = heater.export_dict()

        for id, temp in eqfetch.get_temps().items():
            _eq['temps'][id] = temp.export_dict()

        for id, humidity in eqfetch.get_humiditys().items():
            _eq['humiditys'][id] = humidity.export_dict()

        self.wfile.write(bytes(json.dumps(data,
                                          sort_keys=True,
                                          indent=4), 'utf-8'))


def serve_forever():
    print("starting REST server...")
    httpd = HTTPServer(('0.0.0.0', 9999), RESTHTTPRequestHandler)
    print("probably on...")
    httpd.serve_forever()
