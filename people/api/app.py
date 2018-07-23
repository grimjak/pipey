import os
import json
from flask import Flask, redirect, url_for, request, render_template, jsonify
from pymongo import MongoClient
from bson import json_util
from flask_cors import CORS

app = Flask(__name__)
# enable CORS
CORS(app)


#client = MongoClient(
#    os.environ['DB_PORT_27017_TCP_ADDR'],
#    27017)
client = MongoClient(
    'db',
    27017)

db = client.people


@app.route('/')
def todo():

    _items = db.people.find()
    items = [item for item in _items]

    return render_template('people.html', items=items)


@app.route('/new', methods=['POST'])
def new():

    item_doc = {
        'name': request.form['name'],
        'description': request.form['description'],
        'employeeNumber': request.form['employeeNumber']
    }
    db.people.insert_one(item_doc)

    return redirect(url_for('todo'))

@app.route('/people')
def people():
    data = [json.dumps(item, default=json_util.default) for item in db.people.find(projection={'_id':False})]
    return json.dumps(data)

#figure out how to return just the keys, ultimately need keys plus metadata for building input UI
@app.route('/keys')
def keys():
    data = list(db.people.find(projection={'_id':False}))
    keys = set().union(*[d.keys() for d in list(db.people.find(projection={'_id':False}))])
    return json.dumps(list(keys))

@app.route('/columns')
def columns():
    data = db.people.aggregate([{
                        "$project": { 
                            "name": { "$type": "$name" }
                        }
                    }])
    for d in data:
        print d
    return json.dumps(list(data))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)