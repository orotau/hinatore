from flask import Flask, render_template, flash, \
make_response, request, redirect, url_for
from random import shuffle
import datetime
import hinatore_db
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' #copied
positions = ["nw", "ne", "se", "sw"]
ui_data = {}

@app.route('/')
def home():
    # get the list of users and list of question groups
    # for initial selection
    users = hinatore_db.get_users()
    question_groups = hinatore_db.get_question_groups()
    return render_template('home.html', users=users, question_groups=question_groups)

@app.route('/start', methods=['POST'])
def start():
    # Used to gather the data from the home screen
    # set cookies and get the process underway
    response = make_response(redirect(url_for('question', \
        group=request.form["question_group"], \
        number=1, \
        total=4 \
        )))
    response.set_cookie("user", request.form["user"])
    response.set_cookie("start_time", datetime.datetime.now().isoformat())
    return response


@app.route('/<group>/<number>/<total>')
def question(group, number, total):
    db_qas = hinatore_db.get_data(group, number)
    shuffle(positions)
    ui_data[positions[0]] = (db_qas['correct_answer'], "ca")
    ui_data[positions[1]] = (db_qas['wrong_answer_a'], "wa")
    ui_data[positions[2]] = (db_qas['wrong_answer_b'], "wb")
    ui_data[positions[3]] = (db_qas['wrong_answer_c'], "wc")

    # to allow correct positioning on answer.html
    # flash(message, category)
    flash('correct_answer', positions[0])
    flash('wrong_answer_a', positions[1])
    flash('wrong_answer_b', positions[2])
    flash('wrong_answer_c', positions[3])

    question = db_qas['question']
    return render_template('question.html', question=question, ui_data=ui_data)

@app.route('/<group>/<number>/<total>/<selection>')
def answer(group, number, total, selection):
    '''
    We are displaying the answer page, given the users selection
    We are also writing the results of the selection
    (correct vs incorrect) to the database
    '''
    # get data to display
    db_qas = hinatore_db.get_data(group, number)

    # write result to database
    print(request.cookies.get("user"))
    print(request.cookies.get("start_time"))
    return render_template('answer.html', selection=selection, db_qas=db_qas)

@app.route('/<group>/<number>/<total>/hinatore')
def hinatore(group, number, total):
    response = make_response(render_template('hinatore.html'))
    #response.delete_cookie("user")
    #response.delete_cookie("start_time")
    return response

if __name__ == '__main__':
    # http://flask.pocoo.org/docs/1.0/api/#flask.Flask.run
    app.run(debug=True)
