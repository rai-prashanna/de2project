from flask import (Flask, jsonify, Markup, render_template)
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

def get_db():
    client = MongoClient(host='test_mongodb',
                         port=27017)
    db = client["aggregation"]
    return db

@app.route('/')
def ping_server():
    return "Welcome to Flask Server of Data Engineering."

@app.route('/languages')
def get_results_q1():
    db = get_db()
    result = db.aggregation.findOne({type: "Q1"}).sort({timestamp:1})
    return render_template('result_q1.html', result=result)

if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000)
