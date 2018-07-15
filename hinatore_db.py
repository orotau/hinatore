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
