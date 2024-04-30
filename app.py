from flask import Flask
app = Flask(__name__)
#check whether flask is succesfully installed and running properly
@app.route('/')
def hello_world():
    return "Hello world"