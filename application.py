from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello Gurp!"

@app.route("test")
def testo():
    return "<h1>Dang</h1>"