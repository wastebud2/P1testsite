from flask import Flask, render_template, redirect
from app.travelingSalesman import sortLocations
import json
import firebase_admin
from firebase_admin import credentials, db



## Setup ##
app = Flask(__name__)
cred = credentials.Certificate("firebase_service_key.json")
firebase = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://affladsruter.firebaseio.com/'
})
ref = db.reference('affaldsruter')



## Routes ##
@app.route("/")
def index():
    snapshot = ref.order_by_key().get().items()
    for key, val in snapshot:
        print("Key: {0}, value: {1}".format(key, val))
    return 'fis og ballade'
    #return render_template('index.html', entries=snapshot)


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
