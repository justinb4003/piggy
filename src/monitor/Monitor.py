import db.EqFetch as eqfetch

from task.Heating import Heating
from task.Cooling import Cooling

def execute():
	for id, vent in eqfetch.get_vents().items():
		vent.print_status()
		pass

	for id, heater in eqfetch.get_heaters().items():
		heater.print_status()

	for id, temp in eqfetch.get_temps().items():
		temp.print_status()

	for id, humidity in eqfetch.get_humiditys().items():
		humidity.print_status()

	heating = Heating()
	if heating.want_action() == False:
		print("Heating makes no call.")
	else:
		print("Heating taking action.")
		heating.take_action()

	cooling = Cooling()
	if cooling.want_action() == False:
		print("Cooling makes no call.")
	else:
		print("Cooling taking action.")
		cooling.take_action()

