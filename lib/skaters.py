__author__ = "Mitchell Elliott"
__credits__ = "Mitchell Elliott and Jason Cockroft"
__status__ = "Development"

""" 
skaters.py
Pulls NHL playoff game stats for skaters from the NHL stats API and puts
them in the skaters table in the pool database.
"""

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from lib.jhp import *
import requests

year = "20192020"

def create_skaters_table():
    global year
    db = db_connect("jhpDB")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM nhl_teams")
    teams = cursor.fetchall()

    BASE = "http://statsapi.web.nhl.com/api/v1"
    active = 5

    sql ='''CREATE TABLE IF NOT EXISTS skaters(
        player_id INT PRIMARY KEY,
        player_name CHAR(25),
        team_id TINYINT(1),
        team_name CHAR(25),
        goals SMALLINT,
        assists SMALLINT,
        points SMALLINT,
        status_id TINYINT(1)
    )'''

    db_create_table("jhpDB", sql)

    for team in teams:
        team_id = team[0]
        team_name = team[1]
        team_status = team[2]
        if team_status == active:
            status_id = 1
        else:
            status_id = 0

        roster = requests.get("{}/teams/{}/roster".format(BASE, team_id)).json()

        if "roster" in roster:
            for player in roster['roster']:
                player_id = player['person']['id']
                player_name = player['person']['fullName']
                position = player['position']['code']

                if position != "G":
                    goals = 0
                    assists = 0
                    points = 0
                    print(player_id)

                    sql = "INSERT INTO skaters (player_id, player_name, team_id, team_name, goals, assists, points, status_id) \
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    val = (player_id, player_name, team_id, team_name, goals, assists, points, status_id)
                    cursor.execute(sql, val)
                    db.commit()

    db.close()

def update_skaters_table():
    global year
    db = db_connect("jhpDB")
    cursor = db.cursor(buffered=True)
    cursor.execute("SELECT * FROM nhl_teams")
    teams = cursor.fetchall()

    BASE = "http://statsapi.web.nhl.com/api/v1"
    active = 5

    for team in teams:
        team_id = team[0]
        team_name = team[1]
        team_status = team[2]
        if team_status == active:
            status_id = 1
        else:
            status_id = 0

        roster = requests.get("{}/teams/{}/roster".format(BASE, team_id)).json()

        if "roster" in roster:
            for player in roster['roster']:
                player_id = player['person']['id']
                player_name = player['person']['fullName']
                position = player['position']['code']

                if position != "G":
                    goals = 0
                    assists = 0
                    points = 0

                    sql = "SELECT * FROM skaters WHERE player_id = '{id}'".format(id=player_id)
                    cursor.execute(sql)
                    fetch = cursor.fetchone()

                    if fetch is not None:
                        stats = requests.get("{}/people/{}/stats?stats=statsSingleSeasonPlayoffs&season={}".format(BASE, player_id, year)).json()

                        if stats['stats'][0]['splits']:
                            goals = stats['stats'][0]['splits'][0]['stat']['goals']
                            assists = stats['stats'][0]['splits'][0]['stat']['assists']
                            points = stats['stats'][0]['splits'][0]['stat']['points']

                            sql = "UPDATE skaters SET goals = {g}, assists = {a}, points = {p}, status_id = {s_id} WHERE player_id = '{p_id}'" \
                            .format(g=goals, a=assists, p=points, s_id=status_id, p_id=player_id)
                            cursor.execute(sql)
                            db.commit()

    db.close()

def get_skater_stats(player_id):
    db = db_connect("jhpDB")
    cursor = db.cursor()
    sql = "SELECT * FROM skaters WHERE player_id = '{id}'".format(id=player_id)
    cursor.execute(sql)
    stats = cursor.fetchone()
    db.commit()
    db.close()
    return stats
