from flask import Flask, render_template, redirect
import pymongo
from app.travelingSalesman import sortLocations
import json
import time

## Setup ##
app = Flask(__name__)
mongoclient = pymongo.MongoClient("mongodb+srv://test:1234@test-wbvkk.azure.mongodb.net/test?retryWrites=true&w=majority") 
db = mongoclient["testbase"]
db_entries = db["test_col"]

## Routes ##
@app.route("/")
def index():
    return render_template('index.html', entries=db_entries)

@app.route('/update/<int:pk>/<float:fill>/')
def update(pk, fill):
    try:
        db_entries.update_one({'pk':pk},{ "$set": {'fill':fill}}, upsert=False)
        return "Success!"
    except:
        return "An error occurred"

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

if __name__ == "__main__":
    app.run(debug=True)