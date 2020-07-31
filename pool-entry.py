__author__ = "Mitchell Elliott"
__credits__ = "Mitchell Elliott and Jason Cockroft"
__status__ = "Development"

""" pool-entry.py
    Manages the creation and insertion of pool teams into the pool database
"""

import jhp
import requests

entry_id = 0

def create_entry_table():
    sql = '''CREATE TABLE IF NOT EXISTS pool_entries ( 
           entry_id SMALLINT PRIMARY KEY, 
           team_name CHAR(25), 
           gm_name CHAR(25), 
           email CHAR(25), 
           hometown CHAR(25),
           country CHAR(3),
           pay_status CHAR(25), 
           pay_method CHAR(25), 
           pay_amount TINYINT(1) 
        )'''

    jhp.db_create_table("poolDB", sql)

def create_stats_table():
    sql = '''CREATE TABLE IF NOT EXISTS pool_stats ( 
           entry_id SMALLINT PRIMARY KEY, 
           curr_rank SMALLINT,
           prev_rank SMALLINT,
           team_name CHAR(25), 
           num_act_players TINYINT(1),
           points SMALLINT,
           points_change SMALLINT,
           num_duds SMALLINT,
           prize SMALLINT
        )'''

    jhp.db_create_table("poolDB", sql)

def create_roster_table(team_name):
    db = jhp.db_connect("poolDB")
    cursor = db.cursor()

    sql ='''CREATE TABLE IF NOT EXISTS {table_name} (
       player_id INT PRIMARY KEY,
       player_name CHAR(25)
    )'''.format(table_name=team_name)

    cursor.execute(sql)
    db.commit()
    db.close()

def create_pool_entry(entry_stats):
    global entry_id
    entry_id += 1
    db = jhp.db_connect("poolDB")
    cursor = db.cursor()
    sql = "INSERT INTO pool_entries (entry_id, team_name, gm_name, email, hometown, country, pay_status, pay_method, pay_amount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (entry_id, entry_stats[0], entry_stats[1], entry_stats[2], entry_stats[3], entry_stats[4], entry_stats[5], entry_stats[6], entry_stats[7])
    cursor.execute(sql, val)
    sql = "INSERT INTO pool_stats (entry_id, curr_rank, prev_rank, team_name, num_act_players, points, points_change, num_duds, prize) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (entry_id, 0, 0, entry_stats[0], 0, 0, 0, 0, 0)
    cursor.execute(sql, val)
    create_roster_table(entry_stats[0])
    db.commit()
    db.close()

def update_pool_entry(team_name, column, value):
    db = jhp.db_connect("poolDB")
    cursor = db.cursor()
    sql = "UPDATE pool_entries SET {col} = {val} WHERE team_name = {name}".format(col=column, val=value, name=team_name)
    cursor.execute(sql)
    db.commit()
    db.close()

def update_team_stats(team_name, column, value):
    db = jhp.db_connect("poolDB")
    cursor = db.cursor()
    sql = "UPDATE pool_stats SET {col} = {val} WHERE team_name = {name}".format(col=column, val=value, name=team_name)
    cursor.execute(sql)
    db.commit()
    db.close()
