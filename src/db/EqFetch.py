#!/usr/bin/python3

import pymysql

from subsystem.Vent import Vent 
from subsystem.Heater import Heater 

vents = {}
heaters = {}


def execute_sql(sql):
	db = pymysql.connect("localhost", "root", "nothing", "ircon")
	cursor = db.cursor()
	cursor.execute(sql)
	results = cursor.fetchall()
	db.close()
	return results

def load_all():
	results = execute_sql("SELECT short_name FROM eq_vent ORDER BY short_name ")
	for row in results:
		print("Loading vent %s" % ( row[0] ) )
		get_vent(row[0])

	results = execute_sql("SELECT short_name FROM eq_heater ORDER BY short_name ")
	for row in results:
		print("Loading heater %s" % ( row[0] ) )
		get_heater(row[0])
	

def get(type, id):
	if (type == "vent"):
		return get_vent(id)
	if (type == "heater"):
		return get_heater(id)

def get_vents():
	return vents

def get_heaters():
	return heaters

def get_vent(id):
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

def get_heater(id):
	if (id in heaters):
		return heaters[id]

	db = pymysql.connect("localhost", "root", "nothing", "ircon")
	cursor = db.cursor()
	cursor.execute("SELECT full_name, short_name, on_io_uri " + 
				   " FROM eq_heater " + 
				   "WHERE short_name = '%s'" % id) 
	results = cursor.fetchall()
	for row in results:
		print("full = %s and short = %s" % ( row[0], row[1] ) )
		res = Heater(row[0], row[1], row[2])	
	db.close()

	heaters[id] = res
	return res
