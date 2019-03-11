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


## TODO: The giant massive TODO list

### IO:
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

