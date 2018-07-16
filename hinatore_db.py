import sqlite3
from os import path

ROOT = path.dirname(path.realpath(__file__))
db_path = path.join(ROOT, "hinatore.db")

def get_data(group, number):
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row # makes a named tuple
    cur = con.cursor()
    query = '''
    SELECT
        *
    FROM
        question_and_answers
    WHERE
        question_group = ?
        AND question_number = ?
    '''
    vars = (group, number)

    with con:
        cur.execute(query, vars)
        return cur.fetchall()[0]

def get_users():
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row # makes a named tuple
    cur = con.cursor()
    query = '''
    SELECT
        name
    FROM
        person
    '''

    with con:
        cur.execute(query)
        return cur.fetchall()

def get_question_groups():
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row # makes a named tuple
    cur = con.cursor()
    query = '''
    SELECT DISTINCT
        question_group
    FROM
        question_and_answers
    '''

    with con:
        cur.execute(query)
        return cur.fetchall()
