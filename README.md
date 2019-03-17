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

If I have my requirements.txt built right you should be able to install all the
project deps with:
`pip3 install -r src/requirements.txt`

The ircon_full.sql file contains a sample MySQL/MariaDB database dump.  Loading
this will create some basic equipment and sensors that point right back to the
URLs that the stock simulator currently uses.  By default the system wants to
connect to:  
database: ircon  
username: piggy  
password: oinkoink  

Changing connection parameters is done, currently, in `db/EqFetch.py`.

## Runable Files

* `main.py`: This is the main environmental control program. Basically the daemon
  of the system.

* `ghsim.py`: A very basic simulator for greenhouse sensors.  Intended to be
  something more sophisticated later.

* `clidisp.py`: A command line interface to showing the status of the system.

* `disp.py`: Intended to be a GUI interface showing the status of the system but
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

Inside the `schedule` directory we have the various schedulers. There are three
and we've already touched on two of them a little bit.  The first is
haphazardly named 'Scheduler' -- this is the module that runs our command
objects.  It has two simple queues in it.  If you add commanda via
`add_immediate()` the command will start executing, possibly alongside other
commands, immediately on the next loop, which should be around every 10-20ms.
If the command is added to the Scheduler via `add_sequential()` it goes into a
queue where commands are executed until completion and then the next on is run.

The next one we've already touched on is TaskRunner which, surprise surprise,
runs our task objects. In short it loops through acive tasks and calls their
`want_action()` method which returns a tuple containing a True/False value
indicating whether or not the task wants to do anything, and the second value
is a list containing the short names (from the DB) of equipment it would like
to modify. The TaskRunner then ranks tasks by priority and whichever one wins
is allowed to use that device.  The TaskRunner will then call the
`take_action()` method on the action passing it the list of allowed equipment.
It is up to the task to honor this arrangement.  There is currently nothing
preventing it from taking a "rogue" action.

Lastly, at least for now, we have SensorTickle.  Its job is to keep sensor
readings all up to date so that when a task or command wants to read from a
sensor it doesn't have to block for the IO.  It also lets us set up a
monitoring/alert system where if a sensor goes down we'll know about it even if
the tasks aren't using it or smart enough to report the failure. Every sensor
in the system inherits from BaseSubsystem but also BaseSensor.  The BaseSensor
class forces a `_refresh_value()` method to be there.  However if SensorTickle
sees a `_arefresh_value()` method on the object it'll use that as an asynchio
compatiable version.  This interface/contract may change in the figure but it's
working for now.


## TODO: The giant massive TODO list

### IO
The whole IO mechanism needs work. Currently none actually occurs becuase it's
all simulated anyway.  Next step is to get some better simulation (V-REP is on
the radar) but also getting something physical is probably a good idea.

The whole mechanism in the DB where I try and define io is going to go away.
Something far more extensible is needed, but I'm not there yet.

### Configuration
It still needs an interface into the system for configuring equipment, tasks,
schedules, etc.  Everything is still hardcoded.

The internal webservice that runs the REST interface will be used to configure
the system.  It'll be up to the main daemon to send changes back to the DB.
It'll basically just expose the config options via JSON and also take JSON back
to update them.  From there we just make a simple GUI app that can bang on that
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
