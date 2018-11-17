import db.EqFetch as eqfetch

def execute():
	for id, vent in eqfetch.get_vents().items():
		vent.print_status()

	for id, heater in eqfetch.get_heaters().items():
		heater.print_status()

