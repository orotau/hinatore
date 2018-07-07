from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('start.html')

if __name__ == '__main__':
    # http://flask.pocoo.org/docs/1.0/api/#flask.Flask.run
    app.run(debug=True)
