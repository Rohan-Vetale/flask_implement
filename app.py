"""
@Author: Rohan Vetale

@Date: 2024-04-30 12:40

@Last Modified by: Rohan Vetale

@Last Modified time: 2024-04-30 18:50

@Title : Flask main app module
"""
import re
from passlib.hash import sha256_crypt
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from utils import JWT
jwt_handler = JWT()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:123456@localhost/flask_auth_db'
db=SQLAlchemy(app)
 
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(128), nullable=True)
    twitter_id = db.Column(db.String(50), unique=True, nullable=True)
    oauth_token = db.Column(db.String(200), nullable=True)
    oauth_token_secret = db.Column(db.String(200), nullable=True)

    def __init__(self,username,password_hash,email):
        self.username=username
        self.password_hash=password_hash
        self.email=email

    def __repr__(self):
        return '<User %r>' % self.username
 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')
 


@app.route('/submit_register', methods=['POST'])
def submit_register():
    username = request.form['username']
    real_password = request.form['password_hash']
    password_hash = sha256_crypt.hash(real_password)
    email = request.form['email']

    # Validate email format using regex
    if not re.match(r'^[\w\.-]+@[\w\.-]+$', email):
        return render_template('failure.html', data="Invalid email format")

    if username == "" or real_password == "" or email == "":
        return render_template('failure.html', data="Please check the details you have entered")

    user = User(username, password_hash, email)
    db.session.add(user)
    db.session.commit()
    token = jwt_handler.jwt_encode({"user_id" : user.id})
    return render_template('success.html', data=username, token_id=token)


@app.route('/submit_login', methods=['POST'])
def submit_login():
    username=request.form['username']
    real_password=request.form['password_hash'] #Fetching the original password
    if username == "" or real_password == "":
        return render_template('failure.html', data="Please check the details you have entered")
    user_exists = db.session.query(User).filter(User.username==username).one_or_none()
    if not user_exists or not sha256_crypt.verify(real_password,user_exists.password_hash):
        return render_template('failure.html', data="You have entered invalid credentials")
    if user_exists and sha256_crypt.verify(real_password,user_exists.password_hash):
        token = jwt_handler.jwt_encode({"user_id" : user_exists.id})
        return render_template('success.html',token_id=token, data=user_exists.username)
    else:
        return render_template('success.html', data = "Invalid User", token_id = "Invalid token")

if __name__ == "__main__":
    app.run(debug=True)
