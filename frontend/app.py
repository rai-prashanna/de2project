from flask import Flask, jsonify
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
    _q1 = db.animal_tb.find()
    q1 = [{"id": q1["id"], "python": q1["python"], "java": q1["java"], "c":q1["c"]} for q1 in _q1]
    return jsonify({"Q1": q1})

if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000)
