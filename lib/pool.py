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
from lib.current_date import *
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

def create_pool_points_table():
    sql = '''CREATE TABLE IF NOT EXISTS pool_points (
        entry_id SMALLINT PRIMARY KEY AUTO_INCREMENT
    )'''

    db_create_table("jhpDB", sql)

def create_pool_rankings_table():
    sql = '''CREATE TABLE IF NOT EXISTS pool_rankings (
        entry_id SMALLINT PRIMARY KEY AUTO_INCREMENT
    )'''

    db_create_table("jhpDB", sql)

def create_pool():
    create_entry_table()
    create_stats_table()
    create_pool_points_table()
    create_pool_rankings_table()

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
    monthday = get_current_monthday()

    if fetch is None:
        sql = "INSERT INTO pool_entries (entry_name, gm_name, email, hometown, country, pay_status, pay_method, pay_amount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (entry_name, gm_name, email, hometown, country, pay_status, pay_method, pay_amount)
        cursor.execute(sql, val)
        db.commit()
        sql = "INSERT INTO pool_stats (curr_rank, prev_rank, entry_name, num_act_players, points, points_change, num_duds, prize) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (0, 0, entry_name, 0, 0, 0, 0, 0)
        cursor.execute(sql, val)
        db.commit()
        sql = "ALTER TABLE pool_points ADD {col} VARCHAR(4) NOT NULL".format(col=monthday)
        cursor.execute(sql)
        db.commit()
        sql = "INSERT INTO pool_points ({col}) VALUES (%s)"
        val = (0)
        cursor.execute(sql, val)
        db.commit()
        create_roster_table(entry_stats[0])
    
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
    sql = "UPDATE pool_stats SET points = {points} WHERE entry_name = '{team}'".format(points=curr_points, team=entry_name)
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

    db.close()

def update_pool_points_table():
    db = db_connect("jhpDB")
    cursor = db.cursor(buffered=True)
    sql = "SELECT * FROM pool_stats"
    cursor.execute(sql)
    teams = cursor.fetchall()
    monthday = get_current_monthday()
    sql = "SELECT * FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = \
    'jhpDB' AND TABLE_NAME = 'pool_points' AND COLUMN_NAME = \
    '{col}'".format(col=monthday)
    cursor.execute(sql)
    fetch = cursor.fetchone()

    if fetch is None:
        sql = "ALTER TABLE pool_points ADD {col} VARCHAR(4) NOT NULL".format(col=monthday)
        cursor.execute(sql)
        db.commit()
    
    for team in teams:
        entry_id = team[0]
        points = team[5]
        sql = "SELECT entry_id FROM pool_points where entry_id = {id}".format(id=entry_id)
        cursor.execute(sql)
        fetch = cursor.fetchone()

        if fetch is None:
            sql = "INSERT INTO pool_points (entry_id, {col}) VALUES (%s, %s)".format(col=monthday)
            val = (entry_id, points)
            cursor.execute(sql, val)
            db.commit()

        sql = "UPDATE pool_points SET {col} = {pts} WHERE entry_id = '{id}'".format(col=monthday, pts=points, id=entry_id)
        cursor.execute(sql)
        db.commit()

    db.close()

def update_pool_rankings_table():
    db = db_connect("jhpDB")
    cursor = db.cursor(buffered=True)
    sql = "SELECT * FROM pool_stats"
    cursor.execute(sql)
    teams = cursor.fetchall()
    monthday = get_current_monthday()
    sql = "SELECT * FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = \
    'jhpDB' AND TABLE_NAME = 'pool_rankings' AND COLUMN_NAME = \
    '{col}'".format(col=monthday)
    cursor.execute(sql)
    fetch = cursor.fetchone()

    if fetch is None:
        sql = "ALTER TABLE pool_rankings ADD {col} VARCHAR(4) NOT NULL".format(col=monthday)
        cursor.execute(sql)
        db.commit()
    
    for team in teams:
        entry_id = team[0]
        ranking = team[1]
        sql = "SELECT entry_id FROM pool_rankings where entry_id = {id}".format(id=entry_id)
        cursor.execute(sql)
        fetch = cursor.fetchone()

        if fetch is None:
            sql = "INSERT INTO pool_rankings (entry_id, {col}) VALUES (%s, %s)".format(col=monthday)
            val = (entry_id, ranking)
            cursor.execute(sql, val)
            db.commit()

        sql = "UPDATE pool_rankings SET {col} = {rank} WHERE entry_id = '{id}'".format(col=monthday, rank=ranking, id=entry_id)
        cursor.execute(sql)
        db.commit()

    db.close()

def get_pool_points():
    db = db_connect("jhpDB")
    cursor = db.cursor(buffered=True)
    sql = "SELECT entry_id, entry_name, points FROM pool_stats"
    cursor.execute(sql)
    stats = cursor.fetchall()
    db.close()
    return stats

def get_pool_points_ordered():
    db = db_connect("jhpDB")
    cursor = db.cursor(buffered=True)
    sql = "SELECT entry_id, entry_name, points FROM pool_stats ORDER BY points DESC"
    cursor.execute(sql)
    stats = cursor.fetchall()
    db.close()
    return stats

def set_prev_rank_to_curr_rank():
    db = db_connect("jhpDB")
    cursor = db.cursor(buffered=True)
    sql = "SELECT entry_id, curr_rank FROM pool_stats"
    cursor.execute(sql)
    ranks = cursor.fetchall()

    for rank in ranks:
        sql = "UPDATE pool_stats SET prev_rank = {rank} WHERE entry_id = '{id}'".format(rank=rank[1], id=rank[0])
        cursor.execute(sql)
        db.commit()

    db.close()

def update_pool_points_rankings():
    db = db_connect("jhpDB")
    cursor = db.cursor(buffered=True)
    stats = get_pool_points_ordered()

    for i, stat in enumerate(stats, start=1):
        sql = "UPDATE pool_stats SET curr_rank = {rank} WHERE entry_id = '{id}'".format(rank=i, id=stat[0])
        cursor.execute(sql)
        db.commit()
    
    db.close()

def update_active_player_count():
    db = db_connect("jhpDB")
    cursor = db.cursor(buffered=True)
    sql = "SELECT entry_id, entry_name FROM pool_stats"
    cursor.execute(sql)
    teams = cursor.fetchall()

    for team in teams:
        sql = "SELECT player_id FROM {table}".format(table=team[1])
        cursor.execute(sql)
        players = cursor.fetchall()
        active_count = 0

        for player in players:
            sql = "SELECT status_id FROM skaters WHERE player_id = '{id}'".format(id=player[0])
            cursor.execute(sql)
            status_id = cursor.fetchone()
            if status_id is not None and status_id[0] == 5:
                active_count += 1

        sql = "UPDATE pool_stats SET num_act_players = {num} WHERE entry_id = '{id}'".format(num=active_count, id=team[0])
        cursor.execute(sql)
        db.commit()

    db.close()

def update_points_change():
    db = db_connect("jhpDB")
    cursor = db.cursor(buffered=True)
    sql = "SELECT entry_id, points FROM pool_stats"
    cursor.execute(sql)
    teams = cursor.fetchall()
    monthday = get_current_monthday()

    for team in teams:
        curr_points = team[1]
        sql = "SELECT {md} FROM pool_points WHERE entry_id = {id}".format(md=monthday, id=team[0])
        cursor.execute(sql)
        prev_points = cursor.fetchone()
        points_change = curr_points - int(prev_points[0])
        sql = "UPDATE pool_stats SET points_change = {chg} WHERE entry_id = '{id}'".format(chg=points_change, id=team[0])
        cursor.execute(sql)
        db.commit()

    db.close()

def update_dud_count():
    db = db_connect("jhpDB")
    cursor = db.cursor(buffered=True)
    sql = "SELECT entry_id, entry_name FROM pool_stats"
    cursor.execute(sql)
    teams = cursor.fetchall()

    for team in teams:
        sql = "SELECT player_id FROM {table}".format(table=team[1])
        cursor.execute(sql)
        players = cursor.fetchall()
        dud_count = 0

        for player in players:
            sql = "SELECT points FROM skaters WHERE player_id = '{id}'".format(id=player[0])
            cursor.execute(sql)
            points = cursor.fetchone()
            if points is not None and points[0] == 0:
                dud_count += 1

        sql = "UPDATE pool_stats SET num_duds = {num} WHERE entry_id = '{id}'".format(num=dud_count, id=team[0])
        cursor.execute(sql)
        db.commit()

    db.close()
    
def get_pool_stats(column, order):
    db = db_connect("jhpDB")
    cursor = db.cursor(buffered=True)
    sql = "SELECT * FROM pool_stats ORDER BY {col} {ord}".format(col=column, ord=order)
    cursor.execute(sql)
    stats = cursor.fetchall()
    return stats

def get_pool_stats_ordered():
    db = db_connect("jhpDB")
    cursor = db.cursor(buffered=True)
    sql = "SELECT * FROM pool_stats ORDER BY points DESC"
    cursor.execute(sql)
    stats = cursor.fetchall()
    db.close()
    return stats

def print_pool_stats(column, order):
    stats = get_pool_stats(column, order)

    print("+----------------------------------------------------------------------------------+")
    print("| Rank | Prev |              Team              | Active | Pts | Chg | Duds | Prize |")

    for row in stats:
        rank = str(row[1]).rjust(4, ' ')
        prev = str(row[2]).rjust(4, ' ')
        team = str(row[3]).ljust(30, ' ')
        active = str(row[4]).rjust(6, ' ')
        points = str(row[5]).rjust(3, ' ')
        change = str(row[6]).rjust(3, ' ')
        duds = str(row[7]).rjust(4, ' ')
        prize = str(row[8]).rjust(5, ' ')
        print("+----------------------------------------------------------------------------------+")
        print("| " + rank + " | " + prev + " | " + team + " | " + active + " | " + points + " | " + change + " | " + duds + " | " + prize + " |")

    print("+----------------------------------------------------------------------------------+")


def print_pool_stats_ordered():
    stats = get_pool_stats_ordered()

    print("+----------------------------------------------------------------------------------+")
    print("| Rank | Prev |              Team              | Active | Pts | Chg | Duds | Prize |")

    for row in stats:
        rank = str(row[1]).rjust(4, ' ')
        prev = str(row[2]).rjust(4, ' ')
        team = str(row[3]).ljust(30, ' ')
        active = str(row[4]).rjust(6, ' ')
        points = str(row[5]).rjust(3, ' ')
        change = str(row[6]).rjust(3, ' ')
        duds = str(row[7]).rjust(4, ' ')
        prize = str(row[8]).rjust(5, ' ')
        print("+----------------------------------------------------------------------------------+")
        print("| " + rank + " | " + prev + " | " + team + " | " + active + " | " + points + " | " + change + " | " + duds + " | " + prize + " |")

    print("+----------------------------------------------------------------------------------+")

def print_pool_points():
    stats = get_pool_points()

    for row in stats:
        print(str(row[1]) + " " + str(row[2]))

def print_pool_points_ordered():
    stats = get_pool_points_ordered()

    for row in stats:
        team = str(row[1]).ljust(20, ' ')
        points = str(row[2])
        print(team + " " + points)
