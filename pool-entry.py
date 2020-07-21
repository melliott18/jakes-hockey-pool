__author__ = "Mitchell Elliott"
__credits__ = "Mitchell Elliott and Jason Cockroft"
__status__ = "Development"

""" pool-entry.py
    Manages the creation and insertion of pool teams into the pool database
"""

import jhp
import requests

jhp.db_create("poolDB")
db = jhp.db_connect("poolDB")
cursor = db.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS poolDB")
cursor.execute("DROP TABLE pool_teams")
cursor.execute("DROP TABLE SuperSlug")

sql = '''CREATE TABLE IF NOT EXISTS pool_teams ( 
       pool_team_id TINYINT(1) PRIMARY KEY, 
       pool_team_name CHAR(25), 
       pool_team_gm_name CHAR(25), 
       pool_team_gm_email CHAR(25), 
       pool_team_gm_hometown CHAR(25),
       pool_team_gm_country CHAR(3),
       pool_team_gm_pay_status CHAR(10), 
       pool_team_gm_pay_method CHAR(25), 
       pool_team_gm_pay_amount TINYINT(1), 
       pool_team_points SMALLINT 
    )'''

cursor.execute(sql)

team_id = 1
team_name = "SuperSlug"
team_gm_name = "Mitchell Elliott"
team_gm_email = "email@gmail.com"
team_gm_hometown = "City Name"
team_gm_country = "USA"
team_gm_pay_status = "Paid"
team_gm_pay_method = "PayPal"
team_gm_pay_amount = 10
team_points = 200

sql = "INSERT INTO pool_teams (pool_team_id, pool_team_name, pool_team_gm_name, pool_team_gm_email, pool_team_gm_hometown, pool_team_gm_pay_status, pool_team_gm_pay_method, pool_team_gm_pay_amount, pool_team_points) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
val = (team_id, team_name, team_gm_name, team_gm_email, team_gm_hometown, team_gm_pay_status, team_gm_pay_method, team_gm_pay_amount, team_points)
cursor.execute(sql, val)

db.commit()

sql ='''CREATE TABLE IF NOT EXISTS {table_name} (
       player_id INT PRIMARY KEY,
       player_name CHAR(25)
    )'''.format(table_name=team_name)

cursor.execute(sql)

db.commit()

BASE = "http://statsapi.web.nhl.com/api/v1"
teams = requests.get("{}/teams".format(BASE)).json()
roster = requests.get("{}/teams/{}/roster".format(BASE, 28)).json()

for player in roster['roster']:
            player_id = player['person']['id']
            player_name = player['person']['fullName']
            print(player_name)
            sql = "INSERT INTO {table_name} (player_id, player_name) VALUES(%s, %s)".format(table_name=team_name)
            val = (player_id, player_name)
            cursor.execute(sql, val)
            db.commit()

query = 'SELECT player_id FROM SuperSlug'

cursor.execute(query)
for row in cursor:
    print(row)     

db.close()
