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
    question_group = request.form["question_group_and_total"].split('|')[0]
    total = request.form["question_group_and_total"].split('|')[1]
    response = make_response(redirect(url_for('question', \
        group=question_group, \
        number=1, \
        total=total \
        )))
    response.set_cookie("user", request.form["user"])
    response.set_cookie("start_time", datetime.datetime.now().isoformat())
    return response


@app.route('/<group>/<number>/<total>')
def question(group, number, total):
    user = request.cookies.get("user")
    dwell_time = hinatore_db.get_dwell_time(user)
    print(user, dwell_time["dwell_time"])
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
    return render_template('question.html', question=question, \
                            ui_data=ui_data,  dwell_time=dwell_time)

@app.route('/<group>/<number>/<total>/<selection>')
def answer(group, number, total, selection):
    '''
    We are displaying the answer page, given the users selection
    We are also writing the results of the selection
    (correct vs incorrect) to the database
    '''
    # get data from database
    db_qas = hinatore_db.get_data(group, number)

    # get result data to write to database
    # name
    result = {}
    result["name"] = request.cookies.get("user")
    result["dt"] = request.cookies.get("start_time")
    result["question_group"] = group
    result["question_number"] = number
    result["question"] = db_qas["question"]
    result["correct_answer"] = db_qas["correct_answer"]
    #answer given
    db_column = request.args.get('db_column', '')
    if db_column == "ca":
        answer_given = db_qas["correct_answer"]
    elif db_column == "wa":
        answer_given = db_qas["wrong_answer_a"]
    elif db_column == "wb":
        answer_given = db_qas["wrong_answer_b"]
    elif db_column == "wc":
        answer_given = db_qas["wrong_answer_c"]
    else:
        answer_given = db_column
    result["answer_given"] = answer_given
    # write result to database
    hinatore_db.insert_result(result)
    return render_template('answer.html', selection=selection, db_qas=db_qas)

@app.route('/<group>/<number>/<total>/hinatore')
def hinatore(group, number, total):
    # write results to screen
    response = make_response(render_template('hinatore.html'))
    response.delete_cookie("user")
    response.delete_cookie("start_time")
    return response

if __name__ == '__main__':
    # http://flask.pocoo.org/docs/1.0/api/#flask.Flask.run
    app.run(debug=True)
