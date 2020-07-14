import requests
import sqlite3
import time

def db_connect(db_name):
	return sqlite3.connect(db_name)

def db_drop_table(db_name, table_name):
	db = db_connect(db_name)
	cursor = db.cursor()
	query = 'DROP TABLE IF EXISTS {}'.format(table_name)
	cursor.execute(query)
	db.commit()

def db_create_table(db_name, sql):
	db = db_connect(db_name)
	cursor = db.cursor()
	cursor.execute(sql)
	db.commit()

start = time.time()

db_drop_table("poolDB.db", "pool_teams")
sql ='''CREATE TABLE pool_teams(
	   [pool_team_id] integer PRIMARY KEY,
	   [pool_team_name] text,
	   [pool_team_gm_name] text,
	   [pool_team_gm_email] text,
	   [pool_team_gm_pay_status] text,
	   [pool_team_gm_name_pay_amount] integer,
	   [pool_team_gm_pay_method] text,
	   [pool_team_points] integer
	)'''
db_create_table("poolDB.db", sql)
db = db_connect("poolDB.db")
cursor = db.cursor()

pool_team_id = 1
pool_team_name = "Wrecking Ball"
pool_team_gm_name = "Mitchell Elliott"
pool_team_gm_email = "email@gmail.com"
pool_team_gm_pay_status = "Paid"
pool_team_gm_pay_amount = 10
pool_team_gm_pay_method = "PayPal"
pool_team_points = 20

cursor.execute("INSERT INTO pool_teams VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (pool_team_id, pool_team_name, pool_team_gm_name, pool_team_gm_email, pool_team_gm_pay_status, pool_team_gm_pay_amount, pool_team_gm_pay_method, pool_team_points))

db.commit()

BASE = "http://statsapi.web.nhl.com/api/v1"
teams = requests.get("{}/teams".format(BASE)).json()
roster = requests.get("{}/teams/{}/roster".format(BASE, 28)).json()

for player in roster['roster']:
			player_id = player['person']['id']
			player_name = player['person']['fullName']
			print(player_name)

