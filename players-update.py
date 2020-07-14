__author__ = "Mitchell Elliott"
__credits__ = "Mitchell Elliott and Jason Cockroft"
__status__ = "Development"

""" player-update.py
	Pulls NHL playoff game stats for players from the NHL
	stats API and puts them in the players database.
"""

import requests
import sqlite3
import time

BASE = "http://statsapi.web.nhl.com/api/v1"
teams = requests.get("{}/teams".format(BASE)).json()

def db_connect():
	return sqlite3.connect('playersDB.db')

def db_drop_table():
	db = db_connect()
	cursor = db.cursor()
	cursor.execute("DROP TABLE IF EXISTS players")
	return cursor

def db_create_table():
	db = db_connect()
	cursor = db.cursor()
	sql ='''CREATE TABLE players(
	   [player_id] integer PRIMARY KEY,
	   [player_name] text,
	   [team_id] integer,
	   [team_name] text,
	   [player_type] text,
	   [goals] integer,
	   [assists] integer,
	   [wins] integer,
	   [shutouts] integer,
	   [points] integer
	)'''
	cursor.execute(sql)
	db.commit()

start = time.time()

db_drop_table()
db_create_table()
db = db_connect()
cursor = db.cursor()

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
					cursor.execute('''INSERT INTO players VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (player_id, player_name, team_id, team_name, player_type, goals, assists, wins, shutouts, points))
				if "wins" in stats['stats'][0]['splits'][0]['stat']:
					player_type = "Goalie"
					goals = None
					assists = None
					wins = stats['stats'][0]['splits'][0]['stat']['wins']
					shutouts = stats['stats'][0]['splits'][0]['stat']['shutouts']
					points = (wins * 2) + shutouts
					cursor.execute('''INSERT INTO players VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (player_id, player_name, team_id, team_name, player_type, goals, assists, wins, shutouts, points))
				db.commit()
				
db.close()

end = time.time()

