import requests
import os
import sys

# from jhp import *
# from constants import *

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from lib.jhp import *
from lib.constants import *
from lib.nhl_teams import *
from lib.skaters import *
from lib.pool import *

db2 = db_connect("jhpDB")
cursor2 = db2.cursor()
cursor2.execute("SELECT * FROM nhl_teams")
teams = cursor2.fetchall()

teamDict = {}

for team in teams:
    team_id = team[0]
    team_name = team[1]
    status_id = team[2]
    teamDict[team_id] = (team_name,status_id)  #create a team dictionary keyed by team_id, values are tuples (name,status)
    
    print(team_id, teamDict[team_id])
   

print(teamDict[19][0], teamDict[19][1], sep=',')

