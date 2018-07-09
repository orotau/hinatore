from flask import Flask, flash
from flask import render_template
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def home():
    flash('b')
    return render_template('start.html')

@app.route('/answer')
def answer():
    return render_template('answer.html')

if __name__ == '__main__':
    # http://flask.pocoo.org/docs/1.0/api/#flask.Flask.run
    app.run(debug=True)
