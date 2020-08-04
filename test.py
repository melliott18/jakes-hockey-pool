__author__ = "Mitchell Elliott"
__credits__ = "Mitchell Elliott and Jason Cockroft"
__status__ = "Development"

""" test.py
    JHP function test file
"""

import requests
import jhp
import players
import pool
import teams

BASE = "http://statsapi.web.nhl.com/api/v1"
db = jhp.db_connect("poolDB")
cursor = db.cursor()

team_name = "SuperSlug"
team_gm_name = "Mitchell Elliott"
team_gm_email = "email@gmail.com"
team_gm_hometown = "City Name"
team_gm_country = "USA"
team_gm_pay_status = "Paid"
team_gm_pay_method = "PayPal"
team_gm_pay_amount = 10
team_points = 200

team_entry = []
team_entry.append(team_name)
team_entry.append(team_gm_name)
team_entry.append(team_gm_email)
team_entry.append(team_gm_hometown)
team_entry.append(team_gm_country)
team_entry.append(team_gm_pay_status)
team_entry.append(team_gm_pay_method)
team_entry.append(team_gm_pay_amount)
print(team_entry)
pool.create_pool_entry(team_entry)
pool.create_roster_table(team_name)

teams = requests.get("{}/teams".format(BASE)).json()
roster = requests.get("{}/teams/{}/roster".format(BASE, 28)).json()

for player in roster['roster']:
            player_id = player['person']['id']
            player_name = player['person']['fullName']
            print(player_name)
            sql = "SELECT player_id FROM {name} WHERE player_id = '{id}'".format(name=team_name, id=player_id)
            cursor.execute(sql)
            fetch = cursor.fetchone()

            if fetch is None:
                sql = "INSERT INTO {table_name} (player_id, player_name) VALUES(%s, %s)".format(table_name=team_name)
                val = (player_id, player_name)
                cursor.execute(sql, val)

            db.commit()

team_name = "Test"
team_gm_name = "Team Name"
team_gm_email = "email@gmail.com"
team_gm_hometown = "City Name"
team_gm_country = "USA"
team_gm_pay_status = "Paid"
team_gm_pay_method = "PayPal"
team_gm_pay_amount = 10
team_points = 300

team_entry = []
team_entry.append(team_name)
team_entry.append(team_gm_name)
team_entry.append(team_gm_email)
team_entry.append(team_gm_hometown)
team_entry.append(team_gm_country)
team_entry.append(team_gm_pay_status)
team_entry.append(team_gm_pay_method)
team_entry.append(team_gm_pay_amount)
print(team_entry)
pool.create_pool_entry(team_entry)
pool.create_roster_table(team_name)

teams = requests.get("{}/teams".format(BASE)).json()
roster = requests.get("{}/teams/{}/roster".format(BASE, 29)).json()

for player in roster['roster']:
            player_id = player['person']['id']
            player_name = player['person']['fullName']
            print(player_name)
            pool.add_player(team_name, player_id, player_name)

team_name = "Test2"
team_gm_name = "Team Name"
team_gm_email = "email@gmail.com"
team_gm_hometown = "City Name"
team_gm_country = "USA"
team_gm_pay_status = "Paid"
team_gm_pay_method = "PayPal"
team_gm_pay_amount = 10
team_points = 300

team_entry = []
team_entry.append(team_name)
team_entry.append(team_gm_name)
team_entry.append(team_gm_email)
team_entry.append(team_gm_hometown)
team_entry.append(team_gm_country)
team_entry.append(team_gm_pay_status)
team_entry.append(team_gm_pay_method)
team_entry.append(team_gm_pay_amount)
print(team_entry)
pool.create_pool_entry(team_entry)
pool.create_roster_table(team_name)

teams = requests.get("{}/teams".format(BASE)).json()
roster = requests.get("{}/teams/{}/roster".format(BASE, 30)).json()

for player in roster['roster']:
            player_id = player['person']['id']
            player_name = player['person']['fullName']
            print(player_name)
            pool.add_player(team_name, player_id, player_name)

team_name = "Test3"
team_gm_name = "Team Name"
team_gm_email = "email@gmail.com"
team_gm_hometown = "City Name"
team_gm_country = "USA"
team_gm_pay_status = "Paid"
team_gm_pay_method = "PayPal"
team_gm_pay_amount = 10
team_points = 300

team_entry = []
team_entry.append(team_name)
team_entry.append(team_gm_name)
team_entry.append(team_gm_email)
team_entry.append(team_gm_hometown)
team_entry.append(team_gm_country)
team_entry.append(team_gm_pay_status)
team_entry.append(team_gm_pay_method)
team_entry.append(team_gm_pay_amount)
print(team_entry)
pool.create_pool_entry(team_entry)
pool.create_roster_table(team_name)

teams = requests.get("{}/teams".format(BASE)).json()
roster = requests.get("{}/teams/{}/roster".format(BASE, 1)).json()

for player in roster['roster']:
            player_id = player['person']['id']
            player_name = player['person']['fullName']
            print(player_name)
            pool.add_player(team_name, player_id, player_name)

