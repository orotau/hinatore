import sqlite3
from os import path

ROOT = path.dirname(path.realpath(__file__))
db_path = path.join(ROOT, "hinatore.db")

def get_data(question_group="2_dice"):
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
    '''
    vars = (question_group,) # note this is a tuple (trailing comma)

    with con:
        cur.execute(query, vars)
        return cur.fetchall()
