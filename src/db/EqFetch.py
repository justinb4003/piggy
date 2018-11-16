#!/usr/bin/python3

import pymysql

from subsystem.Vent import Vent 

vents = {}

def load_all():
	db = pymysql.connect("localhost", "root", "nothing", "ircon")
	cursor = db.cursor()
	cursor.execute("SELECT short_name FROM eq_vent ORDER BY short_name ")
	results = cursor.fetchall()
	for row in results:
		print("Loading vent %s" % ( row[0] ) )
		getVent(row[0])
	db.close()
	

def get(type, id):
	if (type == "vent"):
		return getVent(id)

def getVent(id):
	if (id in vents):
		return vents[id]

	db = pymysql.connect("localhost", "root", "nothing", "ircon")
	cursor = db.cursor()
	cursor.execute("SELECT full_name, short_name, " +
				   " close_io_uri, open_io_uri, stroke_seconds " +
				   " FROM eq_vent " + 
				   "WHERE short_name = '%s'" % id) 
	results = cursor.fetchall()
	for row in results:
		print("full = %s and short = %s" % ( row[0], row[1] ) )
		res = Vent(row[0],
				   row[1],
				   row[2],
				   row[3],
				   row[4])	
	db.close()

	vents[id] = res
	return res
