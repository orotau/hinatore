from flask import Flask, flash
from flask import render_template
import hinatore_db
app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' # for flashing

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/question')
def question():
    hinatore_db.get_data()
    return render_template('question.html')

@app.route('/answer/<selection>')
def answer(selection):
    return render_template('answer.html', selection=selection)

if __name__ == '__main__':
    # http://flask.pocoo.org/docs/1.0/api/#flask.Flask.run
    app.run(debug=True)
