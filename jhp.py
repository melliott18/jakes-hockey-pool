__author__ = "Mitchell Elliott"
__credits__ = "Mitchell Elliott and Jason Cockroft"
__status__ = "Development"

""" jhp.py
    Hockey Pool Module
"""

import keyring
import mysql.connector

host = "localhost"
user = "root"
password = keyring.get_password("MySQL", user)

def db_create(db_name):
    global host, user, password
    db = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )
    cursor = db.cursor()
    sql = "CREATE DATABASE IF NOT EXISTS {db}".format(db=db_name)
    cursor.execute(sql)
    db.commit()
    return db

def db_connect(db_name):
    global host, user, password
    db = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    return db

def db_create_table(db_name, sql):
    global host, user, password
    db = db_connect(db_name)
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()

def db_drop_table(db_name, table_name):
    global host, user, password
    db = db_connect(db_name)
    cursor = db.cursor()
    sql = "DROP TABLE IF EXISTS {table}".format(table=table_name)
    cursor.execute(sql)
    db.commit()
    return cursor

def table_exists(db_name, table_name):
    global host, user, password
    db = db_connect(db_name)
    cursor = db.cursor()
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = '{db}' AND table_name = '{table}'".format(db=db_name, table=table_name)
    cursor.execute(sql)
    if cursor.fetchone() is not None:
        return True
    else:
        return False

def table_empty(db_name, table_name):
    global host, user, password
    if table_exists(db_name, table_name):
        db = db_connect(db_name)
        cursor = db.cursor()
        sql = "SELECT COUNT(*) FROM {table}".format(db=db_name, table=table_name)
        cursor.execute(sql)
        if cursor.fetchone() is None:
            return True
        else:
            return False

def change_team_status(db_name, team_id, status_id):
    db = jhp.db_connect(db_name)
    cursor = db.cursor()
    sql = "UPDATE teams SET status_id = {status} where team_id = {team}".format(status=status_id, team=team_id)
