import requests
import sqlite3
import time

def db_connect():
	return sqlite3.connect('poolDB.db')

def db_drop_table():
	db = db_connect()
	cursor = db.cursor()
	cursor.execute("DROP TABLE IF EXISTS pool_teams")
	return cursor

def db_create_table():
	db = db_connect()
	cursor = db.cursor()
	sql ='''CREATE TABLE pool_teams(
	   [pool_team_id] integer PRIMARY KEY,
	   [pool_team_name] text,
	   [pool_team_gm_name] text,
	   [pool_team_points] integer
	)'''
	cursor.execute(sql)
	db.commit()

start = time.time()

db_drop_table()
db_create_table()
db = db_connect()
cursor = db.cursor()

pool_team_id = 1
pool_team_name = "Wrecking Ball"
pool_team_gm_name = "Mitchell Elliott"
pool_team_points = 10

cursor.execute('''INSERT INTO pool_teams VALUES (?, ?, ?, ?)''', (pool_team_id, pool_team_name, pool_team_gm_name, pool_team_points))

db.commit()

BASE = "http://statsapi.web.nhl.com/api/v1"
teams = requests.get("{}/teams".format(BASE)).json()
roster = requests.get("{}/teams/{}/roster".format(BASE, 28)).json()

for player in roster['roster']:
			player_id = player['person']['id']
			player_name = player['person']['fullName']
			print(player_name)

