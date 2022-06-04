from flask import (Flask, jsonify, Markup, render_template)
import pymongo
from pymongo import MongoClient

app = Flask(__name__) #, static_folder='static/templates/templates_frontend_home')

def get_db():
    client = MongoClient(host='mongodb',
                         port=27017)
    db = client["aggregation"]
    return db

@app.route('/')
def ping_server():
    return render_template('/templates_frontend_home/home.html')

@app.route('/languages')
def get_data_q1():
    db = get_db()
    result = db.aggregation.find_one({'type':'Q1'}, sort=[('timestamp', pymongo.DESCENDING)])
    return render_template('result_q1.html', result=result)

@app.route('/commits')
def get_data_q2():
    db = get_db()
    result = db.aggregation.find_one({'type':'Q2'}, sort=[('timestamp', pymongo.DESCENDING)])
    return render_template('result_q2.html', result=result)

@app.route('/q3')
def get_data_q3():
    db = get_db()
    result = db.aggregation.find_one({'type':'Q3'}, sort=[('timestamp', pymongo.DESCENDING)])
    return render_template('result_q3.html', result=result)

@app.route('/q4')
def get_data_q4():
    db =  get_db()
    result = db.aggregation.find_one({'type': 'Q4'}, sort=[('timestamp',pymongo.DESCENDING)])
    return render_template('result_q4.html', result=result)
if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000)
