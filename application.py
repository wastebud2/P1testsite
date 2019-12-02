from flask import Flask, render_template, redirect
from app.travelingSalesman import sortLocations
import json
import firebase_admin
from firebase_admin import credentials, firestore



## Setup ##
app = Flask(__name__)
cred = credentials.Certificate("firebase_service_key.json")
firebase = firebase_admin.initialize_app(cred)
db = firestore.client()
units_ref = db.collection('enheder')


## Routes ##
@app.route("/")
def index():
    return render_template('index.html', entries=units_ref.stream())

####### Do we still need this function?
'''
@app.route('/update/<int:pk>/<float:fill>/')
def update(pk, fill):
    try:
        db_entries.update_one({'pk':pk},{ "$set": {'fill':fill}}, upsert=False)
        return "Success!"
    except:
        return "An error occurred"
'''

###### Fix sort function
'''
@app.route("/sort/<float:fill>")
def sort(fill):
    locs = []
    for entry in db_entries.find():     
        if entry["fill"] > fill:
            new_entry = [entry["pk"], entry["lat"], entry["lng"]]
            locs.append(new_entry)
    bestOrder = sortLocations(locs)
    locs = locs[::-1] # flip list order
    locs = [locs[i] for i in bestOrder]
    return render_template('sort.html', data=locs)
'''

if __name__ == "__main__":
    app.run(debug=True)
