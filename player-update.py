""" player_point_events.py
	Pulls stats for goals and assists during NHL playoff games from the NHL
	stats API and puts them in an SQLite database in the form of playoff point
	events.
"""

import requests
import sqlite3
import time

def db_connect():
	return sqlite3.connect('PlayerPointEntryDB.db')

def db_drop_table():
	db = db_connect()
	cursor = db.cursor()
	cursor.execute("DROP TABLE IF EXISTS PLAYER_POINT_ENTRIES")
	return cursor

def db_create_table():
	db = db_connect()
	cursor = db.cursor()
	sql ='''CREATE TABLE PLAYER_POINT_ENTRIES(
	   [PLAYER_ID] INTEGER PRIMARY KEY,
	   [PLAYER_NAME] TEXT,
	   [EVENT_TYPE] TEXT,
	   [POINT_VALUE] INTEGER
	)'''
	cursor.execute(sql)
	db.commit()

start = time.time()

BASE = "http://statsapi.web.nhl.com/api/v1"
teams = requests.get("{}/teams".format(BASE)).json()
teamFile = open("teams.txt", 'w')
playerFile = open("players.txt", 'w', newline ='\n')

db_drop_table()

db_create_table()

db = db_connect()

cursor = db.cursor()

playerCount = 0
numMatchups = 16
numGames = 0
playerID = 0

for playoffRound in range(1, 5):
	numMatchups = int(numMatchups / 2)
	for matchupNumber in range(1, numMatchups + 1):
		for gameNumber in range(1, 8):
			game = requests.get("{}/game/2018030{}{}{}/feed/live".format(BASE, playoffRound, matchupNumber, gameNumber)).json()
			if "liveData" in game:
				numGames += 1
				for playNumber, play in enumerate(game['liveData']['plays']['allPlays']):
					if play['result']['event'] == "Goal":
						description = play['result']['description'].split(", ")
						split1 = description[0].split(" (")
						goal = split1[0]
						split2 = description[1].split(": ")
						split3 = split2[1].split(" (")
						assist1 = split3[0]
						try:
							split4 = description[2].split(" (")
							assist2 = split4[0]
						except IndexError:
							assist2 = "none"
						eventString = str(game['gamePk']) + " " + str(playNumber) + " " + "Goal: " + goal						
						cursor.execute('''INSERT INTO PLAYER_POINT_ENTRIES VALUES (?, ?, ?, ?)''', (playerID, goal, "Goal", 1))
						playerID += 1
						if assist1 != "none":
							eventString = str(game['gamePk']) + " " + str(playNumber) + " " + "Assist: " + assist1
							cursor.execute('''INSERT INTO PLAYER_POINT_ENTRIES VALUES (?, ?, ?, ?)''', (playerID, assist1, "Assist", 1))
							playerID += 1
						if assist2 != "none":	
							eventString = str(game['gamePk']) + " " + str(playNumber) + " " + "Assist: " + assist2
							cursor.execute('''INSERT INTO PLAYER_POINT_ENTRIES VALUES (?, ?, ?, ?)''', (playerID, assist2, "Assist", 1))
							playerID += 1
						db.commit()
				
db.close()

end = time.time()

