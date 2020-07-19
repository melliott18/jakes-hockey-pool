__author__ = "Mitchell Elliott"
__credits__ = "Mitchell Elliott and Jason Cockroft"
__status__ = "Development"

""" teams-update.py
	Keeps track of the teams that are currently in the playoffs and stores the
	team statuses in the teams database.
"""

import jhp
import requests

BASE = "http://statsapi.web.nhl.com/api/v1"
teams = requests.get("{}/teams".format(BASE)).json()

jhp.db_create("teams")
sql ='''CREATE TABLE IF NOT EXISTS {table}(
	   team_id TINYINT(1) PRIMARY KEY,
	   team_name CHAR(25),
	   status_id TINYINT(1)
	)'''.format(table="teams")
jhp.db_create_table("teamsDB", "teams", sql)
db = jhp.db_connect("teamsDB")
cursor = db.cursor()

if jhp.table_empty("teamsDB", "teams"):
	for team in teams['teams']:
		team_id = team['id']
		team_name = team['name']

		sql = "INSERT INTO teams (team_id, team_name, status_id) VALUES (%s, %s, %s)"
		val = (team_id, team_name, 5)
		cursor.execute(sql, val)
		db.commit()
			
db.close()
