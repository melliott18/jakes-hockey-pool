__author__ = "Mitchell Elliott"
__credits__ = "Mitchell Elliott and Jason Cockroft"
__status__ = "Development"

""" 
players.py
Pulls NHL playoff game stats for players from the NHL stats API and puts
them in the players table in the pool database.
"""

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from lib.jhp import *
from lib.constants import *
from lib.current_date import *
import requests

year = "20192020"

def create_players_table():
    global year
    db = db_connect("jhpDB")
    cursor = db.cursor(buffered=True)
    cursor.execute("SELECT * FROM nhl_teams")
    teams = cursor.fetchall()

    BASE = "http://statsapi.web.nhl.com/api/v1"

    sql = "SELECT * FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = \
    'jhpDB' AND TABLE_NAME = 'players'"
    cursor.execute(sql)
    fetch = cursor.fetchone()

    if fetch is not None:
        return

    sql ='''CREATE TABLE IF NOT EXISTS players(
        player_id INT PRIMARY KEY,
        player_name CHAR(25),
        team_id TINYINT(1),
        team_abbr CHAR(3),
        team_name CHAR(25),
        games TINYINT(1),
        goals TINYINT(1),
        assists TINYINT(1),
        wins TINYINT(1),
        shutouts TINYINT(1),
        points TINYINT(1),
        today TINYINT(1),
        selected SMALLINT,
        status_id TINYINT(1)
    )'''

    db_create_table("jhpDB", sql)

    for team in teams:
        team_id = team[0]
        team_abbr = team[1]
        team_name = team[2]
        status_id = team[3]

        roster = requests.get("{}/teams/{}/roster".format(BASE, team_id)).json()

        if "roster" in roster:
            for player in roster['roster']:
                player_id = player['person']['id']
                player_name = player['person']['fullName']
                position = player['position']['code']

                if position != "G":
                    games = 0
                    goals = 0
                    assists = 0
                    wins = 0
                    shutouts = 0
                    points = 0
                    today = 0
                    selected = 0

                    sql = "INSERT INTO players (player_id, player_name, team_id, team_abbr, team_name, games, goals, assists, wins, shutouts, points, today, selected, status_id) \
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    val = (player_id, player_name, team_id, team_abbr, team_name, games, goals, assists, wins, shutouts, points, today, selected, status_id)
                    cursor.execute(sql, val)
                    db.commit()

    db.close()

def create_player_points_table():
    sql = '''CREATE TABLE IF NOT EXISTS player_points (
        entry_id SMALLINT PRIMARY KEY AUTO_INCREMENT
    )'''

    db_create_table("jhpDB", sql)

def update_players_table(status):
    global year
    db = db_connect("jhpDB")
    cursor = db.cursor(buffered=True)
    cursor.execute("SELECT * FROM nhl_teams")
    teams = cursor.fetchall()

    BASE = "http://statsapi.web.nhl.com/api/v1"

    for team in teams:
        team_id = team[0]
        team_abbr = team[1]
        team_name = team[2]
        status_id = team[3]

        if status_id == status:
            roster = requests.get("{}/teams/{}/roster".format(BASE, team_id)).json()

            if "roster" in roster:
                for player in roster['roster']:
                    player_id = player['person']['id']
                    player_name = player['person']['fullName']
                    position = player['position']['code']

                    if position != "G":
                        games = 0
                        goals = 0
                        assists = 0
                        wins = 0
                        shutouts = 0
                        points = 0
                        today = 0
                        selected = 0

                        sql = "SELECT * FROM players WHERE player_id = '{id}'".format(id=player_id)
                        cursor.execute(sql)
                        fetch = cursor.fetchone()

                        if fetch is not None:
                            stats = requests.get("{}/people/{}/stats?stats=statsSingleSeasonPlayoffs&season={}".format(BASE, player_id, year)).json()

                            if stats['stats'][0]['splits']:
                                games = stats['stats'][0]['splits'][0]['stat']['games']
                                goals = stats['stats'][0]['splits'][0]['stat']['goals']
                                assists = stats['stats'][0]['splits'][0]['stat']['assists']
                                points = stats['stats'][0]['splits'][0]['stat']['points']

                            print(str(player_id) + " " + str(player_name).ljust(25, ' ') + " " + \
                            str(team_id).rjust(2, ' ') + " " + str(team_abbr) + " " + \
                            str(team_name).ljust(25, ' ') + " " + str(games).rjust(2, ' ') + " " + \
                            str(goals).rjust(2, ' ') + " " + str(assists).rjust(2, ' ')  + " " +  \
                            str(wins).rjust(2, ' ') + " " + str(shutouts).rjust(2, ' ')  + " " +  \
                            str(points).rjust(2, ' ') + " " + str(today).rjust(2, ' ')  + " " +  \
                            str(selected).rjust(2, ' ') + " " + str(status_id).rjust(2, ' '))

                            sql = "UPDATE players SET games = {gp}, goals = {g}, assists = {a}, points = {p}, status_id = {s_id} WHERE player_id = '{p_id}'" \
                            .format(gp=games, g=goals, a=assists, p=points, s_id=status_id, p_id=player_id)
                            cursor.execute(sql)
                            db.commit()

    db.close()

def update_player_statuses():
    global year
    db = db_connect("jhpDB")
    cursor = db.cursor(buffered=True)
    cursor.execute("SELECT * FROM nhl_teams")
    teams = cursor.fetchall()

    BASE = "http://statsapi.web.nhl.com/api/v1"

    for team in teams:
        team_id = team[0]
        team_abbr = team[1]
        team_name = team[2]
        status_id = team[3]

        roster = requests.get("{}/teams/{}/roster".format(BASE, team_id)).json()

        if "roster" in roster:
            for player in roster['roster']:
                player_id = player['person']['id']
                player_name = player['person']['fullName']
                position = player['position']['code']

                if position != "G":
                    sql = "SELECT * FROM players WHERE player_id = '{id}'".format(id=player_id)
                    cursor.execute(sql)
                    fetch = cursor.fetchone()

                    if fetch is not None:
                        sql = "UPDATE players SET status_id = {s_id} WHERE player_id = '{p_id}'" \
                        .format(s_id=status_id, p_id=player_id)
                        cursor.execute(sql)
                        db.commit()

    db.close()

def update_player_points_table():
    db = db_connect("jhpDB")
    cursor = db.cursor(buffered=True)
    sql = "SELECT * FROM skaters"
    cursor.execute(sql)
    teams = cursor.fetchall()
    monthday = get_current_monthday()
    sql = "SELECT * FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = \
    'jhpDB' AND TABLE_NAME = 'player_points' AND COLUMN_NAME = \
    '{col}'".format(col=monthday)
    cursor.execute(sql)
    fetch = cursor.fetchone()

    if fetch is None:
        sql = "ALTER TABLE player_points ADD {col} VARCHAR(4) NOT NULL".format(col=monthday)
        cursor.execute(sql)
        db.commit()
    
    for team in teams:
        player_id = team[0]
        points = team[5]
        sql = "SELECT player_id FROM player_points where entry_id = {id}".format(id=player_id)
        cursor.execute(sql)
        fetch = cursor.fetchone()

        if fetch is None:
            sql = "INSERT INTO player_points (entry_id, {col}) VALUES (%s, %s)".format(col=monthday)
            val = (entry_id, points)
            cursor.execute(sql, val)
            db.commit()

        sql = "UPDATE player_points SET {col} = {pts} WHERE player_id = '{id}'".format(col=monthday, pts=points, id=player_id)
        cursor.execute(sql)
        db.commit()

    db.close()

def get_player_stats(player_id):
    db = db_connect("jhpDB")
    cursor = db.cursor()
    sql = "SELECT * FROM players WHERE player_id = '{id}'".format(id=player_id)
    cursor.execute(sql)
    stats = cursor.fetchone()
    db.commit()
    db.close()
    return stats
