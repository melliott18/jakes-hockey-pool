__author__ = "Mitchell Elliott"
__credits__ = "Mitchell Elliott and Jason Cockroft"
__status__ = "Development"

""" 
stats.py
"""

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from src.jhp import *
from src.players import *

def get_pool_stats(column, order):
    db = db_connect("jhpDB")
    cursor = db.cursor(buffered=True)
    sql = "SELECT * FROM pool_stats ORDER BY {col} {ord}".format(col=column, ord=order)
    cursor.execute(sql)
    stats = cursor.fetchall()
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

def print_pool_team_stats(entry_name):
    db = db_connect("jhpDB")
    cursor = db.cursor(buffered=True)
    sql = "SELECT * FROM pool_entries WHERE entry_name = '{name}'".format(name=entry_name)
    cursor.execute(sql)
    pool_team_entries = cursor.fetchone()
    sql = "SELECT * FROM pool_stats WHERE entry_name = '{name}'".format(name=entry_name)
    cursor.execute(sql)
    pool_team_stats = cursor.fetchone()
    date = get_date()
    print("Date: " + date)
    print("Team: " + pool_team_stats[3])
    print("GM: " + pool_team_entries[2])
    print("Hometown: " + pool_team_entries[4])
    print()
    print("+---------------------------------------------------------------------------------------+")
    print("| Player                    | Team | Games | Goals | Assists | Wins | Shutouts | Points |")
    sql = "SELECT player_id FROM {entry}".format(entry=pool_team_stats[3])
    cursor.execute(sql)
    players = cursor.fetchall()

    for player in players:
        player_id = player[0]
        stats = get_player_stats(player_id)
        #print(stats)
        player = str(stats[1]).ljust(25, ' ')
        team = str(stats[4]).ljust(4, ' ')
        games = str(stats[6]).rjust(5, ' ')
        goals = str(stats[7]).rjust(5, ' ')
        assists = str(stats[8]).rjust(7, ' ')
        wins = str(stats[9]).rjust(4, ' ')
        shutouts = str(stats[10]).rjust(8, ' ')
        points = str(stats[11]).rjust(6, ' ')
        print("+---------------------------------------------------------------------------------------+")
        print("| " + player + " | " + team + " | " + games + " | " + goals + " | " + assists + " | " + wins + " | " + shutouts + " | " + points + " |")

    print("+---------------------------------------------------------------------------------------+")
    print()

def print_all_pool_team_stats():
    db = db_connect("jhpDB")
    cursor = db.cursor(buffered=True)
    sql = "SELECT entry_name FROM pool_entries"
    cursor.execute(sql)
    teams = cursor.fetchall()
    for team in teams:
        entry_name = team[0]
        print_pool_team_stats(entry_name)

    db.close()

