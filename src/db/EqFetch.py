import pymysql

from subsystem.Heater import Heater
from subsystem.Vent import Vent
from subsystem.Curtain import Curtain
from subsystem.Temp import Temp
from subsystem.Sun import Sun
from subsystem.Wind import Wind
from subsystem.RHSensor import RHSensor

from .EquipmentDefError import EquipmentDefError

vents = {}
heaters = {}
curtains = {}

temps = {}
rh_sensors = {}
sun_sensors = {}
wind_sensors = {}


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

    results = execute_sql("SELECT short_name FROM eq_wind_sensor " +
                          "ORDER BY short_name ")
    for row in results:
        print("Loading wind_sensor %s" % (row[0]))
        get_wind_sensor(row[0])


def get_all_sensors():
    return (list(temps.items()) +
            list(rh_sensors.items()) +
            list(wind_sensors.items()) +
            list(sun_sensors.items()))


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


def get_wind_sensors():
    return wind_sensors


def get_vent(id):
    if (id in vents):
        return vents[id]

    results = execute_sql("SELECT full_name, short_name, " +
                          " close_io_uri, open_io_uri, stroke_seconds " +
                          " FROM eq_vent " +
                          "WHERE short_name = '%s'" % id)
    res = None
    for row in results:
        print("full = %s and short = %s" % (row[0], row[1]))
        res = Vent(row[0], row[1], row[2], row[3], row[4])

    if res is None:
        raise EquipmentDefError("Vent {} is not defined.".format(id))

    vents[id] = res
    return res


def get_heater(id):
    if (id in heaters):
        return heaters[id]

    results = execute_sql("SELECT full_name, short_name, on_io_uri " +
                          " FROM eq_heater " +
                          "WHERE short_name = '%s'" % id)
    res = None
    for row in results:
        print("full = %s and short = %s" % (row[0], row[1]))
        res = Heater(row[0], row[1], row[2])

    if res is None:
        raise EquipmentDefError("Heater {} is not defined.".format(id))

    heaters[id] = res
    return res


def get_curtain(id):
    if (id in curtains):
        return curtains[id]

    results = execute_sql("SELECT full_name, short_name, " +
                          " close_io_uri, open_io_uri, stroke_seconds " +
                          " FROM eq_curtain " +
                          "WHERE short_name = '%s'" % id)
    res = None
    for row in results:
        print("full = %s and short = %s" % (row[0], row[1]))
        res = Curtain(row[0], row[1], row[2], row[3], row[4])

    if res is None:
        raise EquipmentDefError("Curtain {} is not defined.".format(id))

    curtains[id] = res
    return res


def get_temp(id):
    if (id in temps):
        return temps[id]

    results = execute_sql("SELECT full_name, short_name, temp_io_uri " +
                          " FROM eq_temp " +
                          "WHERE short_name = '%s'" % id)
    res = None
    for row in results:
        print("full = %s and short = %s" % (row[0], row[1]))
        res = Temp(row[0], row[1], row[2])

    if res is None:
        raise EquipmentDefError("Temp Sensor {} is not defined.".format(id))

    temps[id] = res
    return res


def get_rh_sensor(id):
    if (id in rh_sensors):
        return rh_sensors[id]

    results = execute_sql("SELECT full_name, short_name, rh_sensor_io_uri " +
                          " FROM eq_rh_sensor " +
                          "WHERE short_name = '%s'" % id)
    res = None
    for row in results:
        print("full = %s and short = %s" % (row[0], row[1]))
        res = RHSensor(row[0], row[1], row[2])

    if res is None:
        raise EquipmentDefError("RH Sensor {} is not defined.".format(id))

    rh_sensors[id] = res
    return res


def get_sun_sensor(id):
    if (id in sun_sensors):
        return sun_sensors[id]

    results = execute_sql("SELECT full_name, short_name, sun_io_uri " +
                          " FROM eq_sun_sensor " +
                          "WHERE short_name = '%s'" % id)
    res = None
    for row in results:
        print("full = %s and short = %s" % (row[0], row[1]))
        res = Sun(row[0], row[1], row[2])

    if res is None:
        raise EquipmentDefError("Sun sensor {} is not defined.".format(id))

    sun_sensors[id] = res
    return res


def get_wind_sensor(id):
    if (id in wind_sensors):
        return wind_sensors[id]

    results = execute_sql("SELECT full_name, short_name, wind_io_uri " +
                          " FROM eq_wind_sensor " +
                          "WHERE short_name = '%s'" % id)
    res = None
    for row in results:
        print("full = %s and short = %s" % (row[0], row[1]))
        res = Wind(row[0], row[1], row[2])

    if res is None:
        raise EquipmentDefError("Wind sensor {} is not defined.".format(id))

    wind_sensors[id] = res
    return res
