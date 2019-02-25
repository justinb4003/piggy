#!/usr/bin/python3

from threading import Thread
import gi
import sys
import json
import requests
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject, GLib


class SystemDisplayWindow(Gtk.ApplicationWindow):

    def refresh_click(self, widget):
        print("clickly click.")
        resp = requests.get("http://localhost:9999/")
        data = resp.json()
        eq = data['equipment']
        for h in eq['heaters']:
            print("h IS: {}".format(eq['heaters'][h]['is_on']))
            # TODO: Figure out why this doesn't work.
            # I'm missing something stupid here.
            # print("h IS: {}".format(h['is_on']))

    def __init__(self, app):
        Gtk.Window.__init__(self, title="System Display", application=app)
        self.set_default_size(400, 800)
        self.set_border_width(5)

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        refresh = Gtk.Button.new_with_label("Refresh")
        refresh.connect("clicked", self.refresh_click)
        grid.attach(refresh, 0, 0, 1, 1)
        """
        grid.attach(self.temp_label, 0, 0, 1, 1)
        grid.attach(self.temp_scale, 0, 1, 1, 1)
        grid.attach(self.humidity_label, 0, 2, 1, 1)
        grid.attach(self.humidity_scale, 0, 3, 1, 1)
        """

        self.add(grid)


class SystemDisplayApplication(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        win = SystemDisplayWindow(self)
        win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)


GObject.threads_init()

app = SystemDisplayApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)
