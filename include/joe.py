import requests

from jhp import *
from constants import *

# 8466138 = Joe Thornton
skaterId = str(8466138)
year = "20192020"       # we need to move this to config.py

base_people_url = 'https://statsapi.web.nhl.com/api/v1/people/'
stats_season_url = '/stats/?stats=statsSingleSeason&season='

base_goalie_url = 'https://api.nhle.com/stats/rest/en/goalie/'
goalie_stats_query =  'summary?isAggregate=false&isGame=false&cayenneExp=gameTypeId=3%20and%20seasonId='


def printPlayerData(ID):

    """ Prints player data based on NHL API

    Args:
        int  ID

    Returns:
        None.
    """

    people_url = base_people_url + str(ID)
    stats_url = people_url + stats_season_url + year

    PlayerStatsResponse = requests.get(stats_url)
    PlayerPeopleResponse = requests.get(people_url)

    print(PlayerStatsResponse)
    print(PlayerPeopleResponse)

    statsJson = PlayerStatsResponse.json()
    peopleJson = PlayerPeopleResponse.json()

    print(peopleJson['people'][0]["fullName"],
          peopleJson['people'][0]["currentTeam"]["name"],
          statsJson['stats'][0]["splits"][0]["stat"]["points"],
          sep=', ')


    goalie_url = base_goalie_url + goalie_stats_query + year
    GoalieStatsResponse = requests.get(goalie_url)
    print(GoalieStatsResponse)

#   Gets the complete list of active goalie stats
    GoalieStatsJson = GoalieStatsResponse.json()

    numGoalie = GoalieStatsJson['total']
    print(numGoalie,":","Goalie Name","\t\t","Team Name","\t\t","playerID\t","G A W L S P")

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
            """
            The following 4 lines should be deleted from the final version.
            These were simply added for error checking.  The extra get slows the routine down considerably.
            """
            people_url = base_people_url + str(playerId)
            goaliePeopleResponse = requests.get(people_url)
            goalieJson = goaliePeopleResponse.json()
            teamName = goalieJson['people'][0]["currentTeam"]["name"]

            print(i,":",fullName,"\t\t",teamName,"\t\t",playerId,"\t\t",goals,assists,wins,losses,shutouts,totalPts, sep=' ')
            '''
            There are some issues here that I need to investigate:  I would rather just updat the values that I have on hand
            and avoid looking up new values like player_name, team_id, player_type and status_id.
            Can I just update goals, assists, wins, shutout, points?

            I need a WHERE clause where palyerID == xyz ....
            See players.py   line 205  update statement 

            sql = "INSERT INTO active_players (player_id, player_name, team_id, team_name, player_type, goals, assists, wins, shutouts, points, status_id) \
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (player_id, player_name, team_id, team_name, player_type, goals, assists, wins, shutouts, points, status_id)
            pcursor.execute(sql, val)
            pdb.commit()
            '''
            sql = "UPDATE skaters SET goals = {g}, assists = {a}, points = {p}, status_id = {s_id} WHERE player_id = '{p_id}'" \
                    .format(g=goals, a=assists, p=points, s_id=status_id, p_id=player_id)
            cursor.execute(sql)
            db.commit()


        # api.nhle typically accurately enters the number of entries in the JSON, but I have seen errors.
        except IndexError:
            print("IndexError: i=",i)
            continue


def create_goalie_pTable():
    db = db_connect("JasonDB")
    cursor = db.cursor()

    sql ='''CREATE TABLE IF NOT EXISTS goalies (
        playerId INT PRIMARY KEY,
        fullName CHAR(25),
        teamName CHAR(25),
        goals SMALLINT,
        assists SMALLINT,
        wins SMALLINT,
        shutouts SMALLINT,
        totalPts SMALLINT,
        statusId SMALLINT
    )'''

    db_create_table("JasonDB", sql)

def init_goalie_pTable():
    global year
    db = db_connect("JasonDB")
    cursor = db.cursor()

    #cursor.execute("SELECT * FROM nhl_teams")
    #teams = cursor.fetchall()

    goalie_url = base_goalie_url + goalie_stats_query + year
    GoalieStatsResponse = requests.get(goalie_url)
    print(GoalieStatsResponse)

#   Gets the complete list of active goalie stats
    GoalieStatsJson = GoalieStatsResponse.json()

    numGoalie = GoalieStatsJson['total']
    print(numGoalie,":","Goalie Name","\t\t","Team Name","\t\t","playerId\t\t","G A W L S P")
    
    for i in range(numGoalie):
        try:
            fullName = GoalieStatsJson['data'][i]["goalieFullName"]
            playerId = GoalieStatsJson['data'][i]["playerId"]
            goals = GoalieStatsJson['data'][i]["goals"]
            assists = GoalieStatsJson['data'][i]["assists"]
            wins = GoalieStatsJson['data'][i]["wins"]
            shutouts = GoalieStatsJson['data'][i]["shutouts"]
            totalPts = GoalieStatsJson['data'][i]["goals"]+GoalieStatsJson['data'][i]["assists"]+ 2*(GoalieStatsJson['data'][i]["wins"])+GoalieStatsJson['data'][i]["shutouts"]
            statusId = CON_NOQUAL

            # losses are not required in our playersDB but I used it for error checking
            losses = GoalieStatsJson['data'][i]["losses"]
            """
            The following 4 lines should be deleted from the final version.
            These were simply added for error checking.  The extra get slows the routine down considerably.
            """
            people_url = base_people_url + str(playerId)
            goaliePeopleResponse = requests.get(people_url)
            goalieJson = goaliePeopleResponse.json()
            teamName = goalieJson['people'][0]["currentTeam"]["name"]

            print(i,":",fullName,"\t\t",teamName,"\t\t",playerId,"\t\t",goals,assists,wins,losses,shutouts,totalPts, sep=' ')
            
            sql = "INSERT INTO goalies (playerId,fullName, teamName, goals, assists, wins, shutouts, totalPts, statusId) \
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (playerId, fullName, teamName, goals, assists, wins, shutouts, totalPts, statusId)
            cursor.execute(sql, val)
            db.commit()
            
        # api.nhle typically accurately enters the number of entries in the JSON, but I have seen errors.
        except IndexError:
            print("IndexError: i=",i)
            continue


    db.close()


def main():

#    db_create("JasonDB")

#    printPlayerData(skaterId)

    create_goalie_pTable()
    init_goalie_pTable()

if __name__ == '__main__':
    main()


'''
            sql = "UPDATE goalies SET goals = {g}, assists = {a}, wins= {w}, shutouts = {so}, totalPts = {tp} WHERE playerID = '{p_id}'" \
                    .format(g=goals, a=assists, w=wins, so=shutouts, tp=totalPts, p_id=playerID)
            cursor.execute(sql)
            db.commit()
'''