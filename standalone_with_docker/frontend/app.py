from flask import (Flask, jsonify, Markup, render_template)
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

def get_db():
    client = MongoClient(host='test_mongodb',
                         port=27017, 
                         username='root', 
                         password='pass',
                        authSource="admin")
    db = client["q1"]
    return db

@app.route('/')
def ping_server():
    return "Welcome to Flask Server of Data Engineering."

@app.route('/languages')
def get_stored_animals():
    db = get_db()
    for object in db.lang.find():
        object = object
        exit
    return render_template('result_q1.html', object=object)

if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000)
