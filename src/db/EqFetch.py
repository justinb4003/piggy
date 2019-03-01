#!/usr/bin/python3

import pymysql

from subsystem.Vent import Vent
from subsystem.Temp import Temp
from subsystem.Sun import Sun
from subsystem.RHSensor import RHSensor
from subsystem.Heater import Heater

vents = {}
heaters = {}
curtains = {}
temps = {}
rh_sensors = {}
sun_sensors = {}


def execute_sql(sql):
    # TODO: Yeah some kind of error handling might be a good idea.
    db = pymysql.connect("localhost", "piggy", "oinkoink", "ircon")
    cursor = db.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    db.close()
    return results


def load_all():
    results = execute_sql("SELECT short_name FROM eq_vent " +
                          "ORDER BY short_name ")
    for row in results:
        print("Loading vent %s" % (row[0]))
        get_vent(row[0])

    results = execute_sql("SELECT short_name FROM eq_heater " +
                          "ORDER BY short_name ")
    for row in results:
        print("Loading heater %s" % (row[0]))
        get_heater(row[0])

    results = execute_sql("SELECT short_name FROM eq_curtain " +
                          "ORDER BY short_name ")
    for row in results:
        print("Loading curtain %s" % (row[0]))
        get_curtain(row[0])

    results = execute_sql("SELECT short_name FROM eq_temp " +
                          "ORDER BY short_name ")
    for row in results:
        print("Loading temp %s" % (row[0]))
        get_temp(row[0])

    results = execute_sql("SELECT short_name FROM eq_rh_sensor " +
                          "ORDER BY short_name ")
    for row in results:
        print("Loading rh_sensor %s" % (row[0]))
        get_rh_sensor(row[0])

    results = execute_sql("SELECT short_name FROM eq_sun_sensor " +
                          "ORDER BY short_name ")
    for row in results:
        print("Loading sun_sensor %s" % (row[0]))
        get_sun_sensor(row[0])


def get_vents():
    return vents


def get_heaters():
    return heaters


def get_curtains():
    return curtains


def get_temps():
    return temps


def get_rh_sensors():
    return rh_sensors


def get_sun_sensors():
    return sun_sensors


def get_vent(id):
    if (id in vents):
        return vents[id]

    results = execute_sql("SELECT full_name, short_name, " +
                          " close_io_uri, open_io_uri, stroke_seconds " +
                          " FROM eq_vent " +
                          "WHERE short_name = '%s'" % id)
    for row in results:
        print("full = %s and short = %s" % (row[0], row[1]))
        res = Vent(row[0], row[1], row[2], row[3], row[4])
    vents[id] = res
    return res


def get_heater(id):
    if (id in heaters):
        return heaters[id]

    results = execute_sql("SELECT full_name, short_name, on_io_uri " +
                          " FROM eq_heater " +
                          "WHERE short_name = '%s'" % id)
    for row in results:
        print("full = %s and short = %s" % (row[0], row[1]))
        res = Heater(row[0], row[1], row[2])

    heaters[id] = res
    return res


def get_curtain(id):
    if (id in curtains):
        return curtains[id]

    results = execute_sql("SELECT full_name, short_name, " +
                          " close_io_uri, open_io_uri, stroke_seconds " +
                          " FROM eq_curtain " +
                          "WHERE short_name = '%s'" % id)
    for row in results:
        print("full = %s and short = %s" % (row[0], row[1]))
        res = Vent(row[0], row[1], row[2], row[3], row[4])
    curtains[id] = res
    return res


def get_temp(id):
    if (id in temps):
        return temps[id]

    results = execute_sql("SELECT full_name, short_name, temp_io_uri " +
                          " FROM eq_temp " +
                          "WHERE short_name = '%s'" % id)
    for row in results:
        print("full = %s and short = %s" % (row[0], row[1]))
        res = Temp(row[0], row[1], row[2])

    temps[id] = res
    return res


def get_rh_sensor(id):
    if (id in rh_sensors):
        return rh_sensors[id]

    results = execute_sql("SELECT full_name, short_name, rh_sensor_io_uri " +
                          " FROM eq_rh_sensor " +
                          "WHERE short_name = '%s'" % id)
    for row in results:
        print("full = %s and short = %s" % (row[0], row[1]))
        res = RHSensor(row[0], row[1], row[2])

    rh_sensors[id] = res
    return res


def get_sun_sensor(id):
    if (id in sun_sensors):
        return sun_sensors[id]

    results = execute_sql("SELECT full_name, short_name, sun_io_uri " +
                          " FROM eq_sun_sensor " +
                          "WHERE short_name = '%s'" % id)
    for row in results:
        print("full = %s and short = %s" % (row[0], row[1]))
        res = Sun(row[0], row[1], row[2])

    sun_sensors[id] = res
    return res
