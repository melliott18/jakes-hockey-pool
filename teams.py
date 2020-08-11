__author__ = "Mitchell Elliott"
__credits__ = "Mitchell Elliott and Jason Cockroft"
__status__ = "Development"

""" teams.py
    Keeps track of the teams that are currently in the playoffs and stores the
    team statuses in the teams database.
"""

from jhp import *
import requests

def update_team_status(team_id, status_id):
    db = db_connect("teamsDB")
    cursor = db.cursor()
    sql = "UPDATE teams SET status_id = {status} where team_id = {team}".format(status=status_id, team=team_id)
    cursor.execute(sql)
    db.commit()
    db = db_connect("playersDB")
    cursor = db.cursor()
    sql = "UPDATE all_players SET status_id = {status} where team_id = {team}".format(status=status_id, team=team_id)
    cursor.execute(sql)
    db.commit()
    db.close()

def insert_teams():
    BASE = "http://statsapi.web.nhl.com/api/v1"
    teams = requests.get("{}/teams".format(BASE)).json()

    db_create("teamsDB")
    sql ='''CREATE TABLE IF NOT EXISTS {table}(
            team_id TINYINT(1) PRIMARY KEY,
            team_name CHAR(25),
            status_id TINYINT(1)
        )'''.format(table="teams")
    db_create_table("teamsDB", sql)
    db = db_connect("teamsDB")
    cursor = db.cursor()

    if table_empty("teamsDB", "teams"):
        for team in teams['teams']:
            team_id = team['id']
            team_name = team['name']
            sql = "INSERT INTO teams (team_id, team_name, status_id) VALUES (%s, %s, %s)"
            val = (team_id, team_name, 5)
            cursor.execute(sql, val)
            db.commit()
    			
    db.close()
