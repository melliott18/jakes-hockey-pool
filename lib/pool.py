__author__ = "Mitchell Elliott"
__credits__ = "Mitchell Elliott and Jason Cockroft"
__status__ = "Development"

""" 
pool.py
Manages the creation and insertion of pool teams into the pool database.
"""

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from lib.jhp import *
from lib.skaters import *
import requests

def create_entry_table():
    sql = '''CREATE TABLE IF NOT EXISTS pool_entries (
        entry_id SMALLINT PRIMARY KEY AUTO_INCREMENT,
        entry_name CHAR(25),
        gm_name CHAR(25),
        email CHAR(25),
        hometown CHAR(25),
        country CHAR(3),
        pay_status CHAR(25),
        pay_method CHAR(25),
        pay_amount TINYINT(1) DEFAULT 0
    )'''

    db_create_table("jhpDB", sql)

def create_stats_table():
    sql = '''CREATE TABLE IF NOT EXISTS pool_stats (
        entry_id SMALLINT PRIMARY KEY AUTO_INCREMENT,
        curr_rank SMALLINT,
        prev_rank SMALLINT,
        entry_name CHAR(25),
        num_act_players TINYINT(1) DEFAULT 0,
        points SMALLINT DEFAULT 0,
        points_change SMALLINT DEFAULT 0,
        num_duds SMALLINT DEFAULT 0,
        prize SMALLINT DEFAULT 0
    )'''

    db_create_table("jhpDB", sql)

def create_pool():
    create_entry_table()
    create_stats_table()

def create_roster_table(entry_name):
    db = db_connect("jhpDB")
    cursor = db.cursor()

    sql ='''CREATE TABLE IF NOT EXISTS {table} (
       player_id INT PRIMARY KEY,
       player_name CHAR(25)
    )'''.format(table=entry_name)

    cursor.execute(sql)
    db.commit()
    db.close()

def create_pool_entry(entry_stats):
    db = db_connect("jhpDB")
    cursor = db.cursor()
    entry_name = entry_stats[0]
    gm_name = entry_stats[1]
    email = entry_stats[2]
    hometown = entry_stats[3]
    country = entry_stats[4]
    pay_status = entry_stats[5]
    pay_method = entry_stats[6]
    pay_amount = 0
    sql = "SELECT entry_name FROM pool_entries WHERE entry_name = '{name}'".format(name=entry_name)
    cursor.execute(sql)
    fetch = cursor.fetchone()

    if fetch is None:
        sql = "INSERT INTO pool_entries (entry_name, gm_name, email, hometown, country, pay_status, pay_method, pay_amount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (entry_name, gm_name, email, hometown, country, pay_status, pay_method, pay_amount)
        cursor.execute(sql, val)
        sql = "INSERT INTO pool_stats (curr_rank, prev_rank, entry_name, num_act_players, points, points_change, num_duds, prize) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (0, 0, entry_name, 0, 0, 0, 0, 0)
        cursor.execute(sql, val)
        create_roster_table(entry_stats[0])
    
    db.commit()
    db.close()

def add_player(entry_name, player_id, player_name):
    db = db_connect("jhpDB")
    cursor = db.cursor()
    sql = "SELECT COUNT(*) FROM {table}".format(table=entry_name)
    cursor.execute(sql)
    count = cursor.fetchone()

    if count[0] < 25:
        sql = "SELECT player_id FROM {table} WHERE player_id = '{player}'".format(table=entry_name, player=player_id)
        cursor.execute(sql)
        fetch = cursor.fetchone()

        if fetch is None:
            sql = "INSERT INTO {table} (player_id, player_name) VALUES(%s, %s)".format(table=entry_name)
            val = (player_id, player_name)
            cursor.execute(sql, val)

    db.commit()
    db.close()

def update_pool_entry(entry_name, column, value):
    db = db_connect("jhpDB")
    cursor = db.cursor()
    sql = "UPDATE pool_entries SET {col} = {val} WHERE entry_name = '{name}'".format(col=column, val=value, name=entry_name)
    cursor.execute(sql)
    db.commit()
    db.close()

def update_pool_team_stats(entry_name):
    db = db_connect("jhpDB")
    cursor = db.cursor(buffered=True)
    sql = "SELECT * FROM pool_stats WHERE entry_name = '{name}'".format(name=entry_name)
    cursor.execute(sql)
    pool_team_stats = cursor.fetchone()
    print(pool_team_stats)
    sql = "SELECT player_id FROM {entry}".format(entry=pool_team_stats[3])
    cursor.execute(sql)
    players = cursor.fetchall()
    prev_points = pool_team_stats[5]
    curr_points = 0
    change = 0
    for player in players:
        player_id = player[0]
        stats = get_skater_stats(player_id)

        if stats is not None:
            curr_points += stats[6]

    change = curr_points - prev_points
    #sql = "UPDATE pool_stats SET goals = {g}, assists = {a}, wins = {w}, shutouts = {so}, points = {p}, status_id = {si} WHERE team_name = '{team}'" \
    #.format(g=goals, a=assists, w=wins, so=shutouts, p=points, si=status_id, team=team_name)
    sql = "UPDATE pool_stats SET points = {p} WHERE entry_name = '{team}'".format(p=curr_points, team=entry_name)
    cursor.execute(sql)
    db.commit()
    db.close()

def update_all_pool_team_stats():
    db = db_connect("jhpDB")
    cursor = db.cursor(buffered=True)
    sql = "SELECT entry_name FROM pool_entries"
    cursor.execute(sql)
    teams = cursor.fetchall()
    for team in teams:
        entry_name = team[0]
        update_pool_team_stats(entry_name)

    db.commit()
    db.close()
