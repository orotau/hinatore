from flask import Flask, render_template, flash, \
make_response, request, redirect, url_for
from random import shuffle
import datetime
import hinatore_db
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' #copied
positions = ["nw", "ne", "se", "sw"]
ui_data = {}

# http://flask.pocoo.org/docs/1.0/logging/
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

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
    db_qas = hinatore_db.get_data(group, number)

    # randomise the position of the 4 answers
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
    user = request.cookies.get("user")
    start_time = request.cookies.get("start_time")
    results = hinatore_db.get_results(user, start_time)

    # calculate percentage correct
    number_of_questions = len(results)
    total_correct = 0
    for result in results:
        if result["correct_answer"] == result["answer_given"]:
            total_correct = total_correct + 1
            
    # https://docs.python.org/3.4/library/string.html
    percentage_correct = '{:.0%}'.format(total_correct/number_of_questions)
    summary = {}
    summary["total_correct"] = total_correct
    summary["number_of_questions"] = number_of_questions
    summary["percentage_correct"] = percentage_correct
    response = make_response(render_template('hinatore.html',
                                             results=results,
                                             summary=summary))
    response.delete_cookie("user")
    response.delete_cookie("start_time")
    return response

if __name__ == '__main__':
    # http://flask.pocoo.org/docs/1.0/api/#flask.Flask.run
    app.run(debug=True)
