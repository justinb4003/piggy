#!/usr/bin/python3

# install deps with:
# sudo apt install python-gi python-gi-cairo python3-gi python3-gi-cairo
# gir1.2-gtk-3.0
# Ubuntu 18.04

import gi
import sys
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject, GLib

HTTP_PORT = 9900

current_temp = 99.0
current_rh = 110.0
current_sun = 50


def http_server_loop():
    httpd = HTTPServer(('0.0.0.0', HTTP_PORT), HTTPRequestHandler)
    httpd.serve_forever()


def main_quit():
    global server_thread
    server_thread.stop()


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # ignore logging anything to the screen for hits.

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        data = {}
        if self.path.endswith("temp"):
            data['temp'] = current_temp
        elif self.path.endswith("humidity"):
            data['humidity'] = current_rh
        elif self.path.endswith("sun"):
            data['sun'] = current_sun
        elif self.path.endswith("all"):
            data['humidity'] = current_rh
            data['temp'] = current_temp
            data['sun'] = current_sun
        else:
            data['unknown'] = self.path

        self.wfile.write(bytes(json.dumps(data), 'utf-8'))


class GHSimWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.Window.__init__(self, title="Greenhouse Simualtor",
                            application=app)
        self.set_default_size(400, 300)
        self.set_border_width(5)

        temp_adj = Gtk.Adjustment(72, -20, 120, 1, 1, 1)
        humidity_adj = Gtk.Adjustment(30, 0, 100, 1, 1, 1)
        sun_adj = Gtk.Adjustment(50, 0, 100, 1, 1, 1)

        self.temp_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL,
                                    adjustment=temp_adj)
        self.temp_scale.set_digits(1)
        self.temp_scale.set_hexpand(True)
        self.temp_scale.set_valign(Gtk.Align.START)
        self.temp_scale.connect("value-changed", self.temp_scale_moved)

        self.temp_label = Gtk.Label()
        self.temp_label.set_text("Set Temp...")

        self.humidity_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL,
                                        adjustment=humidity_adj)
        self.humidity_scale.set_digits(1)
        self.humidity_scale.set_hexpand(True)
        self.humidity_scale.set_valign(Gtk.Align.START)
        self.humidity_scale.connect("value-changed", self.humidity_scale_moved)

        self.humidity_label = Gtk.Label()
        self.humidity_label.set_text("Set Humidity...")

        self.sun_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL,
                                   adjustment=sun_adj)
        self.sun_scale.set_digits(1)
        self.sun_scale.set_hexpand(True)
        self.sun_scale.set_valign(Gtk.Align.START)
        self.sun_scale.connect("value-changed", self.sun_scale_moved)

        self.sun_label = Gtk.Label()
        self.sun_label.set_text("Set Sun...")

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.attach(self.temp_label,     0, 0, 1, 1)
        grid.attach(self.temp_scale,     0, 1, 1, 1)
        grid.attach(self.humidity_label, 0, 2, 1, 1)
        grid.attach(self.humidity_scale, 0, 3, 1, 1)
        grid.attach(self.sun_label,      0, 4, 1, 1)
        grid.attach(self.sun_scale,      0, 5, 1, 1)

        self.add(grid)

    def temp_scale_moved(self, event):
        global current_temp
        current_temp = self.temp_scale.get_value()

    def humidity_scale_moved(self, event):
        global current_rh
        current_rh = self.humidity_scale.get_value()

    def sun_scale_moved(self, event):
        global current_sun
        current_sun = self.sun_scale.get_value()


class GHSimApplication(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        win = GHSimWindow(self)
        win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)


GObject.threads_init()
server_thread = Thread(target=http_server_loop)
server_thread.start()

app = GHSimApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)
