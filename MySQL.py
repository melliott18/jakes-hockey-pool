import mysql.connector
import requests

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Mitch1669224",
  database='poolDB'
)

print(mydb)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS poolDB")

#mycursor.execute("SHOW DATABASES")

#for x in mycursor:
#  print(x)

#sql = "CREATE TABLE pool_teams (name VARCHAR(255), address VARCHAR(255))"

mycursor.execute("DROP TABLE pool_teams")
mycursor.execute("DROP TABLE SuperSlug")

sql = '''CREATE TABLE IF NOT EXISTS pool_teams ( 
	   pool_team_id TINYINT(1) PRIMARY KEY, 
	   pool_team_name CHAR(25), 
	   pool_team_gm_name CHAR(25), 
	   pool_team_gm_email CHAR(25), 
	   pool_team_gm_hometown CHAR(25),
	   pool_team_gm_pay_status CHAR(10), 
	   pool_team_gm_pay_method CHAR(25), 
	   pool_team_gm_pay_amount TINYINT(1), 
	   pool_team_points SMALLINT 
	)'''

mycursor.execute(sql)

team_id = 1
team_name = "SuperSlug"
team_gm_name = "Mitchell Elliott"
team_gm_email = "email@gmail.com"
team_gm_hometown = "City Name"
team_gm_pay_status = "Paid"
team_gm_pay_method = "PayPal"
team_gm_pay_amount = 10
team_points = 200

sql = "INSERT INTO pool_teams (pool_team_id, pool_team_name, pool_team_gm_name, pool_team_gm_email, pool_team_gm_hometown, pool_team_gm_pay_status, pool_team_gm_pay_method, pool_team_gm_pay_amount, pool_team_points) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
val = (team_id, team_name, team_gm_name, team_gm_email, team_gm_hometown, team_gm_pay_status, team_gm_pay_method, team_gm_pay_amount, team_points)
mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")

#sql = """CREATE TABLE IF NOT EXISTS new (player_id INT PRIMARY KEY)"""

sql ='''CREATE TABLE IF NOT EXISTS {table_name} (
	   player_id INT PRIMARY KEY
	)'''.format(table_name=team_name)




"""mycursor.execute('''CREATE TABLE {tab}
  (ID INT PRIMARY KEY     NOT NULL,
  NAME           TEXT    NOT NULL,
  AGE            INT     NOT NULL,
  ADDRESS        CHAR(50),
  SALARY         REAL);'''.format(tab=name))
print ("Table created successfully")
"""

mycursor.execute(sql)

#DECLARE @tablename AS nvarchar(10);
#SET @tablename = 'MyTestTable';

mydb.commit()

BASE = "http://statsapi.web.nhl.com/api/v1"
teams = requests.get("{}/teams".format(BASE)).json()
roster = requests.get("{}/teams/{}/roster".format(BASE, 28)).json()

for player in roster['roster']:
			player_id = player['person']['id']
			player_name = player['person']['fullName']
			print(player_name)
			#sql = "INSERT INTO {table_name} ({id})".format(table_name=team_name, id=player_id)
			sql = "INSERT INTO {table_name} (player_id) VALUES(%s)".format(table_name=team_name)
			#sql = "INSERT INTO SuperSlug (player_id) VALUES(%s)"
			mycursor.execute(sql, (player_id,))
			mydb.commit()

query = 'SELECT player_id FROM SuperSlug'

mycursor.execute(query)
for row in mycursor:
	print(row)     

mydb.close()