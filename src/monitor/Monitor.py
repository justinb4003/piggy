import db.EqFetch as eqfetch


def execute():
    for _id, vent in eqfetch.get_vents().items():
        vent.print_status()

    for _id, heater in eqfetch.get_heaters().items():
        heater.print_status()

    for _id, temp in eqfetch.get_temps().items():
        temp.print_status()

    for _id, humidity in eqfetch.get_humiditys().items():
        humidity.print_status()
