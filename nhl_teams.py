__author__ = "Mitchell Elliott"
__credits__ = "Mitchell Elliott and Jason Cockroft"
__status__ = "Development"

""" nhl_teams.py
    Keeps track of the NHL teams that are currently in the playoffs and stores the
    team statuses in the teams database.
"""

from jhp import *
import requests

def create_nhl_teams_table():
    sql ='''CREATE TABLE IF NOT EXISTS {table}(
            team_id TINYINT(1) PRIMARY KEY,
            team_name CHAR(25),
            status_id TINYINT(1)
        )'''.format(table="nhl_teams")
    db_create_table("jhpDB", sql)

def insert_nhl_teams():
    BASE = "http://statsapi.web.nhl.com/api/v1"
    teams = requests.get("{}/teams".format(BASE)).json()
    db = db_connect("jhpDB")
    cursor = db.cursor()

    if db_table_empty("jhpDB", "nhl_teams"):
        for team in teams['teams']:
            team_id = team['id']
            team_name = team['name']
            sql = "INSERT INTO nhl_teams (team_id, team_name, status_id) VALUES (%s, %s, %s)"
            val = (team_id, team_name, 5)
            cursor.execute(sql, val)
            db.commit()
    			
    db.close()

def update_nhl_team_status(team_id, status_id):
    db = db_connect("jhpDB")
    cursor = db.cursor()
    sql = "UPDATE nhl_teams SET status_id = {status} where team_id = {team}".format(status=status_id, team=team_id)
    cursor.execute(sql)
    db.commit()
    sql = "UPDATE skaters SET status_id = {status} where team_id = {team}".format(status=status_id, team=team_id)
    cursor.execute(sql)
    db.commit()
    db.close()

#def update_nhl_team_statuses():