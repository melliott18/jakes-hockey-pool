__author__ = "Mitchell Elliott"
__credits__ = "Mitchell Elliott and Jason Cockroft"
__status__ = "Development"

""" players.py
    Pulls NHL playoff game stats for players from the NHL
    stats API and puts them in the players database.
"""

from jhp import *
import requests
import time

year = "20192020"

def create_all_players_table():
    global year
    pdb = db_connect("playersDB")
    pcursor = pdb.cursor()
    tdb = db_connect("teamsDB")
    tcursor = tdb.cursor()
    tcursor.execute("SELECT * FROM teams")
    teams = tcursor.fetchall()

    BASE = "http://statsapi.web.nhl.com/api/v1"
    active = 5

    sql ='''CREATE TABLE IF NOT EXISTS all_players(
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

    db_create_table("playersDB", sql)

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

                if position == "G":
                    player_type = "Goalie"
                else:
                    player_type = "Skater"

                goals = 0
                assists = 0
                wins = 0
                shutouts = 0
                points = 0

                sql = "INSERT INTO all_players (player_id, player_name, team_id, team_name, player_type, goals, assists, wins, shutouts, points, status_id) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (player_id, player_name, team_id, team_name, player_type, goals, assists, wins, shutouts, points, status_id)
                pcursor.execute(sql, val)
                pdb.commit()

    pdb.close()
    tdb.close()
    print("All players updated")
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time)

def create_active_players_table():
    global year
    pdb = db_connect("playersDB")
    pcursor = pdb.cursor()
    tdb = db_connect("teamsDB")
    tcursor = tdb.cursor()
    tcursor.execute("SELECT * FROM teams")
    teams = tcursor.fetchall()

    BASE = "http://statsapi.web.nhl.com/api/v1"
    active = 5

    sql ='''CREATE TABLE IF NOT EXISTS active_players(
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

    db_create_table("playersDB", sql)

    for team in teams:
        team_id = team[0]
        team_name = team[1]
        team_status = team[2]
        if team_status == active:
            status_id = 1

            roster = requests.get("{}/teams/{}/roster".format(BASE, team_id)).json()

            if "roster" in roster:
                for player in roster['roster']:
                    player_id = player['person']['id']
                    player_name = player['person']['fullName']
                    position = player['position']['code']

                    if position == "G":
                        player_type = "Goalie"
                    else:
                        player_type = "Skater"

                    goals = 0
                    assists = 0
                    wins = 0
                    shutouts = 0
                    points = 0

                    sql = "INSERT INTO active_players (player_id, player_name, team_id, team_name, player_type, goals, assists, wins, shutouts, points, status_id) \
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    val = (player_id, player_name, team_id, team_name, player_type, goals, assists, wins, shutouts, points, status_id)
                    pcursor.execute(sql, val)
                    pdb.commit()

    pdb.close()
    tdb.close()

def update_all_players():
    global year
    pdb = db_connect("playersDB")
    pcursor = pdb.cursor(buffered=True)
    tdb = db_connect("teamsDB")
    tcursor = tdb.cursor()
    tcursor.execute("SELECT * FROM teams")
    teams = tcursor.fetchall()

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

                if position == "G":
                    player_type = "Goalie"
                else:
                    player_type = "Skater"

                goals = 0
                assists = 0
                wins = 0
                shutouts = 0
                points = 0

                sql = "SELECT * FROM all_players WHERE player_id = '{id}'".format(id=player_id)
                pcursor.execute(sql)
                fetch = pcursor.fetchone()

                if fetch is not None:
                    stats = requests.get("{}/people/{}/stats?stats=statsSingleSeasonPlayoffs&season={}".format(BASE, player_id, year)).json()

                    if stats['stats'][0]['splits']:
                        if player_type == "Skater":
                            goals = stats['stats'][0]['splits'][0]['stat']['goals']
                            assists = stats['stats'][0]['splits'][0]['stat']['assists']
                            points = stats['stats'][0]['splits'][0]['stat']['points']
                        elif player_type == "Goalie":
                            wins = stats['stats'][0]['splits'][0]['stat']['wins']
                            shutouts = stats['stats'][0]['splits'][0]['stat']['shutouts']
                            points = (wins * 2) + shutouts

                        sql = "UPDATE all_players SET goals = {g}, assists = {a}, wins = {w}, shutouts = {so}, points = {p}, status_id = {s_id} WHERE player_id = '{p_id}'" \
                        .format(g=goals, a=assists, w=wins, so=shutouts, p=points, s_id=status_id, p_id=player_id)
                        pcursor.execute(sql)
                        pdb.commit()

    pdb.close()
    tdb.close()
    print("All players updated")
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time)

def update_active_players():
    global year
    pdb = db_connect("playersDB")
    pcursor = pdb.cursor()
    tdb = db_connect("teamsDB")
    tcursor = tdb.cursor()
    tcursor.execute("SELECT * FROM teams")
    teams = tcursor.fetchall()

    BASE = "http://statsapi.web.nhl.com/api/v1"
    active = 5

    schedule = requests.get("{}/schedule".format(BASE)).json()

    for team in teams:
        team_id = team[0]
        team_name = team[1]
        team_status = team[2]
        if team_status == active:
            status_id = 1

            roster = requests.get("{}/teams/{}/roster".format(BASE, team_id)).json()

            if "roster" in roster:
                for player in roster['roster']:
                    player_id = player['person']['id']
                    player_name = player['person']['fullName']
                    position = player['position']['code']

                    if position == "G":
                        player_type = "Goalie"
                    else:
                        player_type = "Skater"

                    goals = 0
                    assists = 0
                    wins = 0
                    shutouts = 0
                    points = 0

                    sql = "SELECT * FROM all_players WHERE player_id = '{id}'".format(id=player_id)
                    pcursor.execute(sql)
                    fetch = pcursor.fetchone()
                    
                    if fetch is not None:
                        stats = requests.get("{}/people/{}/stats?stats=statsSingleSeasonPlayoffs&season={}".format(BASE, player_id, year)).json()

                        if stats['stats'][0]['splits']:
                            if player_type == "Skater":
                                goals = stats['stats'][0]['splits'][0]['stat']['goals']
                                assists = stats['stats'][0]['splits'][0]['stat']['assists']
                                points = stats['stats'][0]['splits'][0]['stat']['points']
                            elif player_type == "Goalie":
                                wins = stats['stats'][0]['splits'][0]['stat']['wins']
                                shutouts = stats['stats'][0]['splits'][0]['stat']['shutouts']
                                points = (wins * 2) + shutouts

                            sql = "UPDATE active_players SET goals = {g}, assists = {a}, wins = {w}, shutouts = {so}, points = {p}, status_id = {s_id} WHERE player_id = '{p_id}'" \
                            .format(g=goals, a=assists, w=wins, so=shutouts, p=points, s_id=status_id, p_id=player_id)
                            pcursor.execute(sql)
                            pdb.commit()

    pdb.close()
    tdb.close()
    print("All players updated")
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time)

def optimized_update():
    global year
    pdb = db_connect("playersDB")
    pcursor = pdb.cursor(buffered=True)
    tdb = db_connect("teamsDB")
    tcursor = tdb.cursor()

    BASE = "http://statsapi.web.nhl.com/api/v1"

    schedule = requests.get("{}/schedule".format(BASE)).json()

    active_teams = []

    for game in schedule['dates'][0]['games']:
        if game['status']['statusCode'] == "3" or game['status']['statusCode'] == "4":
            active_teams.append(game['teams']['away']['team']['id'])
            active_teams.append(game['teams']['home']['team']['id'])

    for active_team in active_teams:
        sql = "SELECT * FROM teams WHERE team_id = '{id}'".format(id=active_team)
        tcursor.execute(sql)
        team = tcursor.fetchone()
        team_id = team[0]
        team_name = team[1]
        team_status = team[2]

        print(team_name)

        roster = requests.get("{}/teams/{}/roster".format(BASE, team_id)).json()

        if "roster" in roster:
            for player in roster['roster']:
                player_id = player['person']['id']
                player_name = player['person']['fullName']
                position = player['position']['code']

                if position == "G":
                    player_type = "Goalie"
                else:
                    player_type = "Skater"

                goals = 0
                assists = 0
                wins = 0
                shutouts = 0
                points = 0

                sql = "SELECT * FROM all_players WHERE player_id = '{id}'".format(id=player_id)
                pcursor.execute(sql)
                fetch = pcursor.fetchone()

                if fetch is not None:
                    stats = requests.get("{}/people/{}/stats?stats=statsSingleSeasonPlayoffs&season={}".format(BASE, player_id, year)).json()

                    if stats['stats'][0]['splits']:
                        if player_type == "Skater":
                            goals = stats['stats'][0]['splits'][0]['stat']['goals']
                            assists = stats['stats'][0]['splits'][0]['stat']['assists']
                            points = stats['stats'][0]['splits'][0]['stat']['points']
                        elif player_type == "Goalie":
                            wins = stats['stats'][0]['splits'][0]['stat']['wins']
                            shutouts = stats['stats'][0]['splits'][0]['stat']['shutouts']
                            points = (wins * 2) + shutouts

                        sql = "UPDATE all_players SET goals = {g}, assists = {a}, wins = {w}, shutouts = {so}, points = {p} WHERE player_id = '{p_id}'" \
                        .format(g=goals, a=assists, w=wins, so=shutouts, p=points, p_id=player_id)
                        pcursor.execute(sql)
                        pdb.commit()

    pdb.close()
    tdb.close()
    print("All players updated")
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time)

def get_player_stats(player_id):
    db = db_connect("playersDB")
    cursor = db.cursor()
    sql = "SELECT * FROM all_players WHERE player_id = '{id}'".format(id=player_id)
    cursor.execute(sql)
    stats = cursor.fetchone()
    db.commit()
    db.close()
    return stats

#def print_all_players():
