__author__ = "Mitchell Elliott"
__credits__ = "Mitchell Elliott and Jason Cockroft"
__status__ = "Development"

""" teams-update.py
	Keeps track of the teams that are currently in the playoffs and stores the
	team statuses in the teams database.
"""

import mysql.connector
import requests

BASE = "http://statsapi.web.nhl.com/api/v1"
teams = requests.get("{}/teams".format(BASE)).json()

def db_create(db_name, host, user, password):
	db = mysql.connector.connect(
		host=host,
		user=user,
		password=password
	)
	cursor = db.cursor()
	sql = "CREATE DATABASE IF NOT EXISTS {db}".format(db=db_name)
	cursor.execute(sql)
	db.commit()
	return db

def db_connect(db_name):
	db = mysql.connector.connect(
		host="localhost",
		user="root",
		password="Mitch1669224",
		database=db_name
	)
	return db

def db_create_table(db_name, table_name, sql):
	db = db_connect(db_name)
	cursor = db.cursor()
	cursor.execute(sql)
	db.commit()

def db_drop_table(db_name, table_name):
	db = db_connect(db_name)
	cursor = db.cursor()
	sql = "DROP TABLE IF EXISTS {table}".format(table=table_name)
	cursor.execute(sql)
	db.commit()
	return cursor

def table_exists(db_name, table_name):
	sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = '{db}' AND table_name = '{table}'".format(db=db_name, table=table_name)
	cursor.execute(sql)
	if cursor.fetchone() is not None:
		return True
	else:
		return False

db_create("teamsDB", "localhost", "root", "Mitch1669224")
sql ='''CREATE TABLE IF NOT EXISTS {table}(
	   team_id TINYINT(1) PRIMARY KEY,
	   team_name CHAR(25),
	   status_id TINYINT(1),
	   status_verbose CHAR(25)
	)'''.format(table="teams")
db_create_table("teamsDB", "teams", sql)
db = db_connect("teamsDB")
cursor = db.cursor()

if not table_exists("teamsDB", "teams"):
	for team in teams['teams']:
		team_id = team['id']
		team_name = team['name']

		sql = "INSERT INTO teams (team_id, team_name, status_id, status_verbose) VALUES (%s, %s, %s, %s)"
		val = (team_id, team_name, 0, "DNQ")
		cursor.execute(sql, val)
		db.commit()
			
db.close()
