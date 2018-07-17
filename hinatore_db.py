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
    SELECT
        question_group,
        count(*) as count
    FROM
        question_and_answers
    GROUP BY
        question_group
    '''

    with con:
        cur.execute(query)
        return cur.fetchall()

def get_dwell_time(user):
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row # makes a named tuple
    cur = con.cursor()
    query = '''
    SELECT
        dwell_time
    FROM
        person
    WHERE
        name = ?
    '''
    vars = (user,)

    with con:
        cur.execute(query, vars)
        return cur.fetchall()[0]

def insert_result(result):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    query = '''
    INSERT INTO
        results (name,
                 dt,
                 question_group,
                 question_number,
                 question,
                 correct_answer,
                 answer_given)
    VALUES
        (?, ?, ?, ?, ?, ?, ?)
    '''
    vars = (result["name"],
            result["dt"],
            result["question_group"],
            result["question_number"],
            result["question"],
            result["correct_answer"],
            result["answer_given"])
    with con:
        cur.execute(query, vars)
        return True

def get_results(user, start_time):
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row # makes a named tuple
    cur = con.cursor()
    query = '''
    SELECT
        *
    FROM
        results
    WHERE
        name = ?
        AND dt = ?
    '''
    vars = (user, start_time)

    with con:
        cur.execute(query, vars)
        return cur.fetchall()
