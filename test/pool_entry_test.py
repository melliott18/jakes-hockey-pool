__author__ = "Mitchell Elliott"
__credits__ = "Mitchell Elliott and Jason Cockroft"
__status__ = "Development"

""" 
pool_entry_test.py
Pool entry test file
"""

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from lib.jhp import *
from lib.skaters import *
from lib.pool import *
from lib.nhl_teams import *
import requests

BASE = "http://statsapi.web.nhl.com/api/v1"
db = db_connect("jhpDB")
cursor = db.cursor()

team_name = "NewYorkIslanders"
team_gm_name = "NYI"
team_gm_email = ""
team_gm_hometown = ""
team_gm_country = "USA"
team_gm_pay_status = ""
team_gm_pay_method = ""
team_gm_pay_amount = 0

team_entry = []
team_entry.append(team_name)
team_entry.append(team_gm_name)
team_entry.append(team_gm_email)
team_entry.append(team_gm_hometown)
team_entry.append(team_gm_country)
team_entry.append(team_gm_pay_status)
team_entry.append(team_gm_pay_method)

print(team_entry)
create_pool_entry(team_entry)
create_roster_table(team_name)

teams = requests.get("{}/teams".format(BASE)).json()
roster = requests.get("{}/teams/{}/roster".format(BASE, 2)).json()

for player in roster['roster']:
            player_id = player['person']['id']
            player_name = player['person']['fullName']
            print(player_name)
            add_player(team_name, player_id, player_name)

team_name = "PhiladelphiaFlyers"
team_gm_name = "PHI"
team_gm_email = ""
team_gm_hometown = ""
team_gm_country = "USA"
team_gm_pay_status = ""
team_gm_pay_method = ""

team_entry = []
team_entry.append(team_name)
team_entry.append(team_gm_name)
team_entry.append(team_gm_email)
team_entry.append(team_gm_hometown)
team_entry.append(team_gm_country)
team_entry.append(team_gm_pay_status)
team_entry.append(team_gm_pay_method)

print(team_entry)
create_pool_entry(team_entry)
create_roster_table(team_name)

roster = requests.get("{}/teams/{}/roster".format(BASE, 4)).json()

for player in roster['roster']:
            player_id = player['person']['id']
            player_name = player['person']['fullName']
            print(player_name)
            add_player(team_name, player_id, player_name)

team_name = "BostonBruins"
team_gm_name = "BOS"
team_gm_email = ""
team_gm_hometown = ""
team_gm_country = "USA"
team_gm_pay_status = ""
team_gm_pay_method = ""

team_entry = []
team_entry.append(team_name)
team_entry.append(team_gm_name)
team_entry.append(team_gm_email)
team_entry.append(team_gm_hometown)
team_entry.append(team_gm_country)
team_entry.append(team_gm_pay_status)
team_entry.append(team_gm_pay_method)

print(team_entry)
create_pool_entry(team_entry)
create_roster_table(team_name)

roster = requests.get("{}/teams/{}/roster".format(BASE, 6)).json()

for player in roster['roster']:
            player_id = player['person']['id']
            player_name = player['person']['fullName']
            print(player_name)
            add_player(team_name, player_id, player_name)

team_name = "MontrealCanadiens"
team_gm_name = "MTL"
team_gm_email = ""
team_gm_hometown = ""
team_gm_country = "CAN"
team_gm_pay_status = ""
team_gm_pay_method = ""

team_entry = []
team_entry.append(team_name)
team_entry.append(team_gm_name)
team_entry.append(team_gm_email)
team_entry.append(team_gm_hometown)
team_entry.append(team_gm_country)
team_entry.append(team_gm_pay_status)
team_entry.append(team_gm_pay_method)

print(team_entry)
create_pool_entry(team_entry)
create_roster_table(team_name)

roster = requests.get("{}/teams/{}/roster".format(BASE, 8)).json()

for player in roster['roster']:
            player_id = player['person']['id']
            player_name = player['person']['fullName']
            print(player_name)
            add_player(team_name, player_id, player_name)

team_name = "CarolinaHurricanes"
team_gm_name = "CAR"
team_gm_email = ""
team_gm_hometown = ""
team_gm_country = "USA"
team_gm_pay_status = ""
team_gm_pay_method = ""

team_entry = []
team_entry.append(team_name)
team_entry.append(team_gm_name)
team_entry.append(team_gm_email)
team_entry.append(team_gm_hometown)
team_entry.append(team_gm_country)
team_entry.append(team_gm_pay_status)
team_entry.append(team_gm_pay_method)

print(team_entry)
create_pool_entry(team_entry)
create_roster_table(team_name)

roster = requests.get("{}/teams/{}/roster".format(BASE, 12)).json()

for player in roster['roster']:
            player_id = player['person']['id']
            player_name = player['person']['fullName']
            print(player_name)
            add_player(team_name, player_id, player_name)

team_name = "TampaBayLightning"
team_gm_name = "TBL"
team_gm_email = ""
team_gm_hometown = ""
team_gm_country = "USA"
team_gm_pay_status = ""
team_gm_pay_method = ""

team_entry = []
team_entry.append(team_name)
team_entry.append(team_gm_name)
team_entry.append(team_gm_email)
team_entry.append(team_gm_hometown)
team_entry.append(team_gm_country)
team_entry.append(team_gm_pay_status)
team_entry.append(team_gm_pay_method)

print(team_entry)
create_pool_entry(team_entry)
create_roster_table(team_name)

roster = requests.get("{}/teams/{}/roster".format(BASE, 14)).json()

for player in roster['roster']:
            player_id = player['person']['id']
            player_name = player['person']['fullName']
            print(player_name)
            add_player(team_name, player_id, player_name)

team_name = "WashingtonCapitals"
team_gm_name = "WSH"
team_gm_email = ""
team_gm_hometown = ""
team_gm_country = "USA"
team_gm_pay_status = ""
team_gm_pay_method = ""

team_entry = []
team_entry.append(team_name)
team_entry.append(team_gm_name)
team_entry.append(team_gm_email)
team_entry.append(team_gm_hometown)
team_entry.append(team_gm_country)
team_entry.append(team_gm_pay_status)
team_entry.append(team_gm_pay_method)

print(team_entry)
create_pool_entry(team_entry)
create_roster_table(team_name)

roster = requests.get("{}/teams/{}/roster".format(BASE, 15)).json()

for player in roster['roster']:
            player_id = player['person']['id']
            player_name = player['person']['fullName']
            print(player_name)
            add_player(team_name, player_id, player_name)

team_name = "ChicagoBlackhawks"
team_gm_name = "CHI"
team_gm_email = ""
team_gm_hometown = ""
team_gm_country = "USA"
team_gm_pay_status = ""
team_gm_pay_method = ""

team_entry = []
team_entry.append(team_name)
team_entry.append(team_gm_name)
team_entry.append(team_gm_email)
team_entry.append(team_gm_hometown)
team_entry.append(team_gm_country)
team_entry.append(team_gm_pay_status)
team_entry.append(team_gm_pay_method)

print(team_entry)
create_pool_entry(team_entry)
create_roster_table(team_name)

roster = requests.get("{}/teams/{}/roster".format(BASE, 16)).json()

for player in roster['roster']:
            player_id = player['person']['id']
            player_name = player['person']['fullName']
            print(player_name)
            add_player(team_name, player_id, player_name)

team_name = "StLouisBlues"
team_gm_name = "STL"
team_gm_email = ""
team_gm_hometown = ""
team_gm_country = "USA"
team_gm_pay_status = ""
team_gm_pay_method = ""

team_entry = []
team_entry.append(team_name)
team_entry.append(team_gm_name)
team_entry.append(team_gm_email)
team_entry.append(team_gm_hometown)
team_entry.append(team_gm_country)
team_entry.append(team_gm_pay_status)
team_entry.append(team_gm_pay_method)

print(team_entry)
create_pool_entry(team_entry)
create_roster_table(team_name)

roster = requests.get("{}/teams/{}/roster".format(BASE, 19)).json()

for player in roster['roster']:
            player_id = player['person']['id']
            player_name = player['person']['fullName']
            print(player_name)
            add_player(team_name, player_id, player_name)

team_name = "CalgaryFlames"
team_gm_name = "CGY"
team_gm_email = ""
team_gm_hometown = ""
team_gm_country = "CAN"
team_gm_pay_status = ""
team_gm_pay_method = ""

team_entry = []
team_entry.append(team_name)
team_entry.append(team_gm_name)
team_entry.append(team_gm_email)
team_entry.append(team_gm_hometown)
team_entry.append(team_gm_country)
team_entry.append(team_gm_pay_status)
team_entry.append(team_gm_pay_method)

print(team_entry)
create_pool_entry(team_entry)
create_roster_table(team_name)

roster = requests.get("{}/teams/{}/roster".format(BASE, 20)).json()

for player in roster['roster']:
            player_id = player['person']['id']
            player_name = player['person']['fullName']
            print(player_name)
            add_player(team_name, player_id, player_name)

team_name = "ColoradoAvalanche"
team_gm_name = "COL"
team_gm_email = ""
team_gm_hometown = ""
team_gm_country = "USA"
team_gm_pay_status = ""
team_gm_pay_method = ""

team_entry = []
team_entry.append(team_name)
team_entry.append(team_gm_name)
team_entry.append(team_gm_email)
team_entry.append(team_gm_hometown)
team_entry.append(team_gm_country)
team_entry.append(team_gm_pay_status)
team_entry.append(team_gm_pay_method)

print(team_entry)
create_pool_entry(team_entry)
create_roster_table(team_name)

roster = requests.get("{}/teams/{}/roster".format(BASE, 21)).json()

for player in roster['roster']:
            player_id = player['person']['id']
            player_name = player['person']['fullName']
            print(player_name)
            add_player(team_name, player_id, player_name)

team_name = "VancouverCanucks"
team_gm_name = "VAN"
team_gm_email = ""
team_gm_hometown = ""
team_gm_country = "CAN"
team_gm_pay_status = ""
team_gm_pay_method = ""

team_entry = []
team_entry.append(team_name)
team_entry.append(team_gm_name)
team_entry.append(team_gm_email)
team_entry.append(team_gm_hometown)
team_entry.append(team_gm_country)
team_entry.append(team_gm_pay_status)
team_entry.append(team_gm_pay_method)

print(team_entry)
create_pool_entry(team_entry)
create_roster_table(team_name)

roster = requests.get("{}/teams/{}/roster".format(BASE, 23)).json()

for player in roster['roster']:
            player_id = player['person']['id']
            player_name = player['person']['fullName']
            print(player_name)
            add_player(team_name, player_id, player_name)

team_name = "DallasStars"
team_gm_name = "DAL"
team_gm_email = ""
team_gm_hometown = ""
team_gm_country = "USA"
team_gm_pay_status = ""
team_gm_pay_method = ""

team_entry = []
team_entry.append(team_name)
team_entry.append(team_gm_name)
team_entry.append(team_gm_email)
team_entry.append(team_gm_hometown)
team_entry.append(team_gm_country)
team_entry.append(team_gm_pay_status)
team_entry.append(team_gm_pay_method)

print(team_entry)
create_pool_entry(team_entry)
create_roster_table(team_name)

roster = requests.get("{}/teams/{}/roster".format(BASE, 25)).json()

for player in roster['roster']:
            player_id = player['person']['id']
            player_name = player['person']['fullName']
            print(player_name)
            add_player(team_name, player_id, player_name)

team_name = "ColumbusBlueJackets"
team_gm_name = "CBJ"
team_gm_email = ""
team_gm_hometown = ""
team_gm_country = "USA"
team_gm_pay_status = ""
team_gm_pay_method = ""

team_entry = []
team_entry.append(team_name)
team_entry.append(team_gm_name)
team_entry.append(team_gm_email)
team_entry.append(team_gm_hometown)
team_entry.append(team_gm_country)
team_entry.append(team_gm_pay_status)
team_entry.append(team_gm_pay_method)

print(team_entry)
create_pool_entry(team_entry)
create_roster_table(team_name)

roster = requests.get("{}/teams/{}/roster".format(BASE, 29)).json()

for player in roster['roster']:
            player_id = player['person']['id']
            player_name = player['person']['fullName']
            print(player_name)
            add_player(team_name, player_id, player_name)

team_name = "ArizonaCoyotes"
team_gm_name = "ARI"
team_gm_email = ""
team_gm_hometown = ""
team_gm_country = "USA"
team_gm_pay_status = ""
team_gm_pay_method = ""

team_entry = []
team_entry.append(team_name)
team_entry.append(team_gm_name)
team_entry.append(team_gm_email)
team_entry.append(team_gm_hometown)
team_entry.append(team_gm_country)
team_entry.append(team_gm_pay_status)
team_entry.append(team_gm_pay_method)

print(team_entry)
create_pool_entry(team_entry)
create_roster_table(team_name)

roster = requests.get("{}/teams/{}/roster".format(BASE, 53)).json()

for player in roster['roster']:
            player_id = player['person']['id']
            player_name = player['person']['fullName']
            print(player_name)
            add_player(team_name, player_id, player_name)

team_name = "VegasGoldenKnights"
team_gm_name = "VGK"
team_gm_email = ""
team_gm_hometown = ""
team_gm_country = "USA"
team_gm_pay_status = ""
team_gm_pay_method = ""

team_entry = []
team_entry.append(team_name)
team_entry.append(team_gm_name)
team_entry.append(team_gm_email)
team_entry.append(team_gm_hometown)
team_entry.append(team_gm_country)
team_entry.append(team_gm_pay_status)
team_entry.append(team_gm_pay_method)

print(team_entry)
create_pool_entry(team_entry)
create_roster_table(team_name)

roster = requests.get("{}/teams/{}/roster".format(BASE, 54)).json()

for player in roster['roster']:
            player_id = player['person']['id']
            player_name = player['person']['fullName']
            print(player_name)
            add_player(team_name, player_id, player_name)
