# PIGGY
Pi Greenhouse Growing... gy. Piggy.  We're calling this project piggy.

## Setup

There's going to be a whole bunch of python deps to pull in before this will
run but I do not have a requirements.txt built yet.  You'll have to figure it
out as you go.

The ircon_full.sql file contains a sample MySQL/MariaDB database dump.  Loading
this will create some basic equipment and sensors that point right back to the
URLs that the stock simulator currently uses.  By default the system wants to connect to:
database: ircon
username: piggy
password: oinkoink

Changing connection parameters is done, currently, in db/EqFetch.py.


## Runable Files

* main.py: This is the main environmental control program. Basically the daemon
  of the system.

* ghsim.py: A very basic simulator for greenhouse sensors.  Intended to be
  something more sophisticated later.

* clidisp.py: A command line interface to showing the status of the system.

* disp.py: Intended to be a GUI interface showing the status of the system but
  not even really started.


## Project Breakdown
src/ source code
....db/ database specific code
....command/ Any IO that needs multiple steps to it goes into a BaseCommand and
gets managed by a scheduler
....schedule/ This is where the command, sensor, and IO schedulers live
....monitor/ Probably a dead section of code at this point.  It was intended to
be a display for the system but that became an out of process deal.
