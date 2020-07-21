__author__ = "Mitchell Elliott"
__credits__ = "Mitchell Elliott and Jason Cockroft"
__status__ = "Development"

""" players-update.py
    Pulls NHL playoff game stats for players from the NHL
    stats API and puts them in the players database.
"""

import jhp
import os
import requests
import time

def update_all_players():
    pdb = jhp.db_connect("playersDB")
    pcursor = pdb.cursor()
    tdb = jhp.db_connect("teamsDB")
    tcursor = tdb.cursor()
    jhp.db_drop_table("playersDB", "all_players")
    jhp.db_drop_table("playersDB", "active_players")
    sql ='''CREATE TABLE all_players(
        player_id INT PRIMARY KEY,
        player_name CHAR(25),
        team_id TINYINT(1),
        team_name CHAR(25),
        player_type CHAR(25),
        goals SMALLINT,
        assists SMALLINT,
        wins SMALLINT,
        shutouts TINYINT(1),
        points SMALLINT,
        status_id TINYINT(1)
    )'''
    jhp.db_create_table("playersDB", sql)
    sql ='''CREATE TABLE active_players(
        player_id INT PRIMARY KEY,
        player_name CHAR(25),
        team_id TINYINT(1),
        team_name CHAR(25),
        player_type CHAR(25),
        goals SMALLINT,
        assists SMALLINT,
        wins SMALLINT,
        shutouts TINYINT(1),
        points SMALLINT,
        status_id TINYINT(1)
    )'''
    jhp.db_create_table("playersDB", sql)
    tcursor.execute("SELECT * FROM teams")
    teams = tcursor.fetchall()

    BASE = "http://statsapi.web.nhl.com/api/v1"
    year = "20182019"

    for team in teams:
        team_id = team[0]
        team_name = team[1]
        if team[2] == 5:
            status_id = 1
        else:
            status_id = 0

        roster = requests.get("{}/teams/{}/roster".format(BASE, team_id)).json()

        if "roster" in roster:
            for player in roster['roster']:
                player_id = player['person']['id']
                player_name = player['person']['fullName']

                stats = requests.get("{}/people/{}/stats?stats=statsSingleSeasonPlayoffs&season={}".format(BASE, player_id, year)).json()

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

                    sql = "INSERT INTO all_players (player_id, player_name, team_id, team_name, player_type, goals, assists, wins, shutouts, points, status_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    val = (player_id, player_name, team_id, team_name, player_type, goals, assists, wins, shutouts, points, status_id)
                    pcursor.execute(sql, val)

                    if status_id:
                        sql = "INSERT INTO active_players (player_id, player_name, team_id, team_name, player_type, goals, assists, wins, shutouts, points, status_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        val = (player_id, player_name, team_id, team_name, player_type, goals, assists, wins, shutouts, points, status_id)
                        pcursor.execute(sql, val)
                    pdb.commit()
    pdb.close()
    tdb.close()
    print("All players updated")
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time)

def update_active_players():
    jhp.db_drop_table("playersDB", "active_players")
    sql ='''CREATE TABLE active_players(
        player_id INT PRIMARY KEY,
        player_name CHAR(25),
        team_id TINYINT(1),
        team_name CHAR(25),
        player_type CHAR(25),
        goals SMALLINT,
        assists SMALLINT,
        wins SMALLINT,
        shutouts TINYINT(1),
        points SMALLINT,
        status_id TINYINT(1)
    )'''
    jhp.db_create_table("playersDB", sql)
    pdb = jhp.db_connect("playersDB")
    pcursor = pdb.cursor()
    tdb = jhp.db_connect("teamsDB")
    tcursor = tdb.cursor()
    tcursor.execute("SELECT * FROM teams")
    teams = tcursor.fetchall()

    BASE = "http://statsapi.web.nhl.com/api/v1"
    year = "20182019"

    for team in teams:
        team_id = team[0]
        team_name = team[1]
        if team[2] == 5:
            status_id = 1
            roster = requests.get("{}/teams/{}/roster".format(BASE, team_id)).json()

            if "roster" in roster:
                for player in roster['roster']:
                    player_id = player['person']['id']
                    player_name = player['person']['fullName']
                    stats = requests.get("{}/people/{}/stats?stats=statsSingleSeasonPlayoffs&season={}".format(BASE, player_id, year)).json()

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

                        sql = "INSERT INTO active_players (player_id, player_name, team_id, team_name, player_type, goals, assists, wins, shutouts, points, status_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        val = (player_id, player_name, team_id, team_name, player_type, goals, assists, wins, shutouts, points, status_id)
                        pcursor.execute(sql, val)
                        pdb.commit()

    pdb.close()
    tdb.close()
    print("All active players updated")
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time)

#while(True):	
update_all_players()
#update_active_players()
    #time.sleep(600)
