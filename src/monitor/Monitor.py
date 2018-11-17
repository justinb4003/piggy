import db.EqFetch as eqfetch

def execute():
	print("Monitor loop execute() hit.")
	for id, vent in eqfetch.get_vents().items():
		vent.print_status()

