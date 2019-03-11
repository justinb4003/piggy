# PIGGY
Pi Greenhouse Growing... Yeah, I suck at naming things. Piggy.  We're calling
this project piggy.

## Overview
The idea is to build a full greenhouse enviornmental control system that can be
run on a single Raspberry Pi.  Given that the simplest implementations only
need basic relays toggled on and off to control the equipment this is certainly
possible with a single pi and a bit of simple wiring of the GPIO pins to a
relay board and getting some sensors for temperature, humidity, sun, wind, etc.
wired in.

Currently the focus isn't on the actual IO itself, but rather getting the
platform built in a manner that's as extensible as possible without being
absurd.  

The dependency on MySQL/MariaDB currently looks absurd because we're just
putting some basic equipment definitions in there.  Long term this will hold a
lot more runtime configuration as well as an extensive logging system.

There's also no reason this has to run on a pi at all.  If you don't need the
GPIO pins anything will do.  Obviously we're targetting Linux here but you
could probably run in under Windows if you really felt like it. Heck, the
engine could be on a VM in a rack that just makes calls out to a Pi running a
simple HTTP server like we do internally in this project, just to handle the
IO.  Or, more likely, there's a slew of relay boards out there with HTTP
interfaces already.  Just call out to them.

Integrating existing sensors could be done similarly.  Stick a Pi out there and
build a webservice that Piggy can easily read from.  There's also no reason 3rd
party vendors couldn't ship sensors Piggy-capable but keep the source locked
up.  The system intentionally reaches outside itself via HTTP calls to make it
easy to integrate non-GPL code into the project.

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

Launch the ghsim.py program before launching main.py in the default
configuration else you'll get nothing as the system can't read from its
sensors.

## How It Works / What Currently Works

The overall architecture probably won't be too foreign if you've used WPILib's
suite for FIRST Robotics Competition.  This is very much patterened from
experiences in working with that.

We'll start with the `subsystem` directory.  Each class in here corresponds to
a physical device implementation.  So, we have things like Vent, Heater,
Curtain, Temp, RHSensor, etc.  Everything in here should inherent from the
BaseSubsystem class and things that are sensor devices which need to keep the
current value up to date also inherent from the BaseSensor class.  We'll come
back to sensors when we get to scheduling.

Next we should talk about the `command` directory.  A command is something that
can be put in a queue for execution by the command scheduler.  The command's
`execute()` method will get hit however frequently the command scheduler is set
for.  Usually this will be something like every 10-20ms or 50-100 times a
second put another way in the opposite order.  In other words expect this to
run quickly, so don't do anything that will take time in there.  After that
method runs the `is_finished()` method is checked.  If that returns true the
command is done and the scheduler pulls it out of the queue.  That's a rough
overview of how they work.

From here we diverge from anything resembling WPILib.

I suppose the `task` directory should be explained next.  A task is similar to
a command in that it also goes into a queue that is run periodically but this
queue is expected to be run slower, like maybe every 30-60 seconds in a
greenhouse environment.  Where a command is a single-focused task trying to
simply get a piece of equipment to a particular point a task is responsible for
coordinating activities with the system as a whole and driving it toward those
overall goals.  For intance if a cooling task wants to open the vents but the
weather limit task says you can't because there's 80mph winds outside the task
scheduler will figure that out and let them know who gets to use what piece of
equipment.  They then use this knowledge of what they want to do vs what they
can do and insert appropriate command objects into that queue to carry out the
tasks.

Inside the `schedule` directory we have the various schedulers.  Those are
currently best explained just be reading their source code and looking at
main.py.  At the current state of the projct you're going to want to tinker
with them intimately anyway.


## TODO: The giant massive TODO list

### IO
The whole IO mechanism needs work. Currently none actually occurs becuase it's
all simulated anyway.  Next step is to get some better simulation (V-REP is on
the radar) but also getting something physical is probably a good idea.

The whole mechanism in the DB where I try and define io is going to go away.
Something far more extensible is needed, but I'm not there yet.

### Configuration
It still needs an interface into the DB for configuring equipment, tasks,
schedules, etc.  Everything is still hardcoded.

The plan there is to make a Python WSGI app that can either be hosted in-app
(like we already do with bottle for the REST interface) but also something that
you could deploy on Apache on a more suitable server, perhaps something
publically available on the net for central control.  Either way it'll
basically just expose the config options via JSON and also take JSON back to
update them.  From there we just make a simple GUI app that can bang on that
webservice to get it all done.  That should help make the app pretty portable
and I'm currently leading toward WinForms C# for that one just so it's natural
feeling on Windows.  Actually I intend for the config app to be kind of
"disposable" where you can pick and choose from many different ideas.  Mobile,
pure web, C# deskto app, Python GTK app, whatever.  All the logic goes in the
webservice.

### Schedules
Tasks not only need to come dynamicaly from the DB but they also need to be
scheduled, not just by time but also sunrise/sunset offset times.

### Zones
It could take into account grouping equipment into zones so you don't use the
wrong temp sensor for the wrong roof vent, but it's not really required by the
system to do this.  It could run 18 zones just fine without actually being
explicitly told to hold them in a "zone." It probably should for no other
reason that keeping the UI easier.  Internally it doesn't even have to check if
we're mixing zones -- leave that enforcement to the config tools.

### Tasks
Need to figure out a way for them to present an interface to a UI for a "story"
config like: BasicHeating: Turn on [heater] when [temp sensor] goes below [x
deg | x deg from setpoint] and leave on for at least [M] minutes. Turn off same
heater when same temp sensor gets above [x deg | x deg from setpoint].
