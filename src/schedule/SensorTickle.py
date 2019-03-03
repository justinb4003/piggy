import db.EqFetch as eqfetch


def execute():
    for sid, s in eqfetch.get_all_sensors():
        s._refresh_value()
