__author__ = "Mitchell Elliott"
__credits__ = "Mitchell Elliott and Jason Cockroft"
__status__ = "Development"

""" players-update.py
	Pulls NHL playoff game stats for players from the NHL
	stats API and puts them in the players database.
"""

import mysql.connector
import requests
import time

BASE = "http://statsapi.web.nhl.com/api/v1"
teams = requests.get("{}/teams".format(BASE)).json()

def db_create():
	db = mysql.connector.connect(
		host="localhost",
		user="root",
		password="Mitch1669224",
	)
	cursor = db.cursor()
	cursor.execute("CREATE DATABASE IF NOT EXISTS playersDB")
	db.commit()
	return db

def db_connect():
	db = mysql.connector.connect(
		host="localhost",
		user="root",
		password="Mitch1669224",
		database='playersDB'
	)
	return db

def db_drop_table():
	db = db_connect()
	cursor = db.cursor()
	cursor.execute("DROP TABLE IF EXISTS players")
	db.commit()
	return cursor

def db_create_table():
	db = db_connect()
	cursor = db.cursor()
	sql ='''CREATE TABLE players(
	   player_id INT PRIMARY KEY,
	   player_name CHAR(25),
	   team_id TINYINT(1),
	   team_name CHAR(25),
	   player_type CHAR(25),
	   goals SMALLINT,
	   assists SMALLINT,
	   wins SMALLINT,
	   shutouts TINYINT(1),
	   points SMALLINT
	)'''
	cursor.execute(sql)
	db.commit()

start = time.time()

db_create()
count = 1

while(True):	
	db_drop_table()
	db_create_table()
	db = db_connect()
	cursor = db.cursor()

	current = time.time()

	print(current - start)
	count += 1

	for team in teams['teams']:
		team_id = team['id']
		team_name = team['name']
		roster = requests.get("{}/teams/{}/roster".format(BASE, team_id)).json()

		if "roster" in roster:
			for player in roster['roster']:
				player_id = player['person']['id']
				player_name = player['person']['fullName']
				stats = requests.get("{}/people/{}/stats?stats=statsSingleSeasonPlayoffs&season=20182019".format(BASE, player_id)).json()

				if stats['stats'][0]['splits']:
					if "assists" in stats['stats'][0]['splits'][0]['stat']:
						player_type = "Skater"
						goals = stats['stats'][0]['splits'][0]['stat']['goals']
						assists = stats['stats'][0]['splits'][0]['stat']['assists']
						wins = None
						shutouts = None
						points = stats['stats'][0]['splits'][0]['stat']['points']
					elif "wins" in stats['stats'][0]['splits'][0]['stat']:
						player_type = "Goalie"
						goals = None
						assists = None
						wins = stats['stats'][0]['splits'][0]['stat']['wins']
						shutouts = stats['stats'][0]['splits'][0]['stat']['shutouts']
						points = (wins * 2) + shutouts
					sql = "INSERT INTO players (player_id, player_name, team_id, team_name, player_type, goals, assists, wins, shutouts, points) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
					val = (player_id, player_name, team_id, team_name, player_type, goals, assists, wins, shutouts, points)
					cursor.execute(sql, val)
					db.commit()
	#time.sleep(600)
				
db.close()
