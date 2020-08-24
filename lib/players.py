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

from lib.constants import *
from lib.date import *
from lib.jhp import *
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
        player_type CHAR(6),
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
                player_type = "Goalie" if position == "G" else "Skater"
                games = 0
                goals = 0
                assists = 0
                wins = 0
                shutouts = 0
                points = 0
                today = 0
                selected = 0

                sql = "INSERT INTO players (player_id, player_name, player_type, team_id, team_abbr, team_name, games, goals, assists, wins, shutouts, points, today, selected, status_id) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (player_id, player_name, player_type, team_id, team_abbr, team_name, games, goals, assists, wins, shutouts, points, today, selected, status_id)
                cursor.execute(sql, val)
                db.commit()

    db.close()

def create_player_points_table():
    sql = '''CREATE TABLE IF NOT EXISTS player_points (
        entry_id SMALLINT PRIMARY KEY AUTO_INCREMENT
    )'''

    db_create_table("jhpDB", sql)

def update_goalies_in_players(status):
    global year

    base_goalie_url = 'https://api.nhle.com/stats/rest/en/goalie/'
    goalie_stats_query =  'summary?isAggregate=false&isGame=false&cayenneExp=gameTypeId=3%20and%20seasonId='
    base_people_url = 'https://statsapi.web.nhl.com/api/v1/people/'

    # update goalies
    db2 = db_connect("jhpDB")
    cursor2 = db2.cursor()
    cursor2.execute("SELECT * FROM nhl_teams")
    teams = cursor2.fetchall()

    teamDict = {}

    for team in teams:
        team_id = team[0]
        team_abbr = team[1]
        team_name = team[2]
        status_id = team[3]
        teamDict[team_id] = (team_name,status_id) #create a team dictionary keyed by team_id, values are tuples (name,status)

    goalie_url = base_goalie_url + goalie_stats_query + year
    GoalieStatsResponse = requests.get(goalie_url)
    print(GoalieStatsResponse)

#   Gets the complete list of active goalie stats
    GoalieStatsJson = GoalieStatsResponse.json()

    numGoalie = GoalieStatsJson['total']
    print(numGoalie,":","Goalie Name","\t\t","Team Name","\t\t","playerId\t\t","G A W L S P S")
    
    '''
        Basic algorithm: From the nhle-api get the JSON of playoff goalies. Traverse this JSON pulling out each goalie's
        player_id and then looking up their team_id from the apistat.  Once we have the team_id, go to the teams table 
        and determine the team status.  With the stats from nhle-api and the status from teams, update the goalie stats 
        table.
    '''
    for i in range(numGoalie):
        try:
            fullName = GoalieStatsJson['data'][i]["goalieFullName"]
            playerId = GoalieStatsJson['data'][i]["playerId"]
            goals = GoalieStatsJson['data'][i]["goals"]
            assists = GoalieStatsJson['data'][i]["assists"]
            wins = GoalieStatsJson['data'][i]["wins"]
            shutouts = GoalieStatsJson['data'][i]["shutouts"]
            totalPts = GoalieStatsJson['data'][i]["goals"]+GoalieStatsJson['data'][i]["assists"]+ 2*(GoalieStatsJson['data'][i]["wins"])+GoalieStatsJson['data'][i]["shutouts"]

            # losses are not required in our playersDB but I used it for error checking
            losses = GoalieStatsJson['data'][i]["losses"]

            # Retreive teamId from playerId
            people_url = base_people_url + str(playerId)
            goaliePeopleResponse = requests.get(people_url)
            goalieJson = goaliePeopleResponse.json()
            teamName = goalieJson['people'][0]["currentTeam"]["name"]
            teamId = goalieJson['people'][0]["currentTeam"]["id"]

            #retreive team status and assign to player status variable
            pStatus = teamDict[teamId][1]

            print(i,":",fullName,"\t\t",teamName,"\t\t",playerId,"\t\t",goals,assists,wins,losses,shutouts,totalPts,pStatus,sep=' ')
                    
            sql = "UPDATE players SET goals = {g}, assists = {a}, wins= {w}, shutouts = {so}, points = {tp}, status_id = {st} WHERE player_id = '{p_id}'" \
                    .format(g=goals, a=assists, w=wins, so=shutouts, tp=totalPts, st = pStatus, p_id=playerId)

            cursor2.execute(sql)
            db2.commit()
        
        # api.nhle typically accurately enters the number of entries in the JSON, but I have seen errors.
        except IndexError:
            print("IndexError: i=",i)
            continue


    db2.close()

def update_players_table(status):
    global year
    
    update_goalies_in_players(status)

    # update skaters
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

        if status_id == status or status == ALL:
            roster = requests.get("{}/teams/{}/roster".format(BASE, team_id)).json()

            if "roster" in roster:
                for player in roster['roster']:
                    player_id = player['person']['id']
                    sql = "SELECT * FROM players WHERE player_id = '{id}'".format(id=player_id)
                    cursor.execute(sql)
                    fetch = cursor.fetchone()
                    player_name = fetch[1]
                    player_type = fetch[2]
                    games = fetch[6]
                    goals = fetch[7]
                    assists = fetch[8]
                    wins = fetch[9]
                    shutouts = fetch[10]
                    points = fetch[11]
                    today = fetch[12]
                    selected = fetch[13]

                    if fetch is not None:
                        if player_type == "Skater":
                            stats = requests.get("{}/people/{}/stats?stats=statsSingleSeasonPlayoffs&season={}".format(BASE, player_id, year)).json()

                            if stats['stats'][0]['splits']:
                                games = stats['stats'][0]['splits'][0]['stat']['games']
                                goals = stats['stats'][0]['splits'][0]['stat']['goals']
                                assists = stats['stats'][0]['splits'][0]['stat']['assists']
                                points = stats['stats'][0]['splits'][0]['stat']['points']

                            sql = "UPDATE players SET games = {gp}, goals = {g}, assists = {a}, points = {p}, status_id = {s_id} WHERE player_id = '{p_id}'" \
                            .format(gp=games, g=goals, a=assists, p=points, s_id=status_id, p_id=player_id)
                            cursor.execute(sql)
                            db.commit()

                        print(str(player_id) + " " + str(player_name).ljust(25, ' ') + " " + str(player_type).ljust(6, ' ') + " " + \
                        str(team_id).rjust(2, ' ') + " " + str(team_abbr) + " " + str(team_name).ljust(25, ' ') + " " + \
                        str(games).rjust(2, ' ') + " " + str(goals).rjust(2, ' ') + " " + str(assists).rjust(2, ' ')  + " " +  \
                        str(wins).rjust(2, ' ') + " " + str(shutouts).rjust(2, ' ')  + " " +  str(points).rjust(2, ' ') + " " + \
                        str(today).rjust(2, ' ')  + " " +  str(selected).rjust(2, ' ') + " " + str(status_id).rjust(2, ' '))
                    else:
                        sql = "INSERT INTO players (player_id, player_name, player_type, team_id, team_abbr, team_name, games, goals, assists, wins, shutouts, points, today, selected, status_id) \
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        val = (player_id, player_name, player_type, team_id, team_abbr, team_name, games, goals, assists, wins, shutouts, points, today, selected, status_id)
                        cursor.execute(sql, val)
                        db.commit()

                        print(str(player_id) + " " + str(player_name).ljust(25, ' ') + " " + str(player_type).ljust(6, ' ') + " " + \
                        str(team_id).rjust(2, ' ') + " " + str(team_abbr) + " " + str(team_name).ljust(25, ' ') + " " + \
                        str(games).rjust(2, ' ') + " " + str(goals).rjust(2, ' ') + " " + str(assists).rjust(2, ' ')  + " " +  \
                        str(wins).rjust(2, ' ') + " " + str(shutouts).rjust(2, ' ')  + " " +  str(points).rjust(2, ' ') + " " + \
                        str(today).rjust(2, ' ')  + " " +  str(selected).rjust(2, ' ') + " " + str(status_id).rjust(2, ' '))

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
