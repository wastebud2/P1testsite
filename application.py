from flask import Flask, render_template
import pymongo

## Setup ##
app = Flask(__name__)
mongoclient = pymongo.MongoClient("mongodb+srv://test:1234@test-wbvkk.azure.mongodb.net/test?retryWrites=true&w=majority") 
db = mongoclient["testbase"]
db_entries = db["test_col"]

## Routes ##
@app.route("/")
def index():
    #return str(db_entries.find_one({'address': 'Recycling (Mineralvej 23)'})['address'])

    return render_template('index.html', entries=db_entries)

if __name__ == "__main__":
    app.run(debug=True)