from flask import Flask, render_template, flash
from random import shuffle
import hinatore_db
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' #copied
positions = ["nw", "ne", "se", "sw"]
db_data = {}
ui_data = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/<group>/<number>/<total>')
def question(group, number, total):
    db_qas = hinatore_db.get_data(group, number)
    shuffle(positions)
    ui_data[positions[0]] = db_qas['correct_answer']
    ui_data[positions[1]] = db_qas['wrong_answer_a']
    ui_data[positions[2]] = db_qas['wrong_answer_b']
    ui_data[positions[3]] = db_qas['wrong_answer_c']

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
    db_qas = hinatore_db.get_data(group, number)
    return render_template('answer.html', selection=selection, db_qas=db_qas)

if __name__ == '__main__':
    # http://flask.pocoo.org/docs/1.0/api/#flask.Flask.run
    app.run(debug=True)
