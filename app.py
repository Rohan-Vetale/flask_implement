"""
@Author: Rohan Vetale

@Date: 2024-04-30 12:40

@Last Modified by: Rohan Vetale

@Last Modified time: 2024-04-30 18:50

@Title : Flask main app module
"""
import re
from passlib.hash import sha256_crypt
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from utils import JWT
from flask_dance.contrib.google import google , make_google_blueprint
from settings import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_SCOPE, APP_SECRET_KEY, SQLALCHEMY_DATABASE_URI

jwt_handler = JWT()
app = Flask(__name__)
app.secret_key = APP_SECRET_KEY
google_blueprint = make_google_blueprint(client_id=GOOGLE_CLIENT_ID,client_secret=GOOGLE_CLIENT_SECRET, scope=["https://www.googleapis.com/auth/userinfo.profile","https://www.googleapis.com/auth/userinfo.email","openid"])
app.register_blueprint(google_blueprint, url_prefix = '/google_login')
app.config['SQLALCHEMY_DATABASE_URI']=SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(128), nullable=True)

    def __init__(self, username, password_hash, email):
        self.username = username
        self.password_hash = password_hash
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username
    
@app.route('/')
def index():
    """
    Description: This function is for rendering the home page.
    Parameter: None
    Return: render_template of index.html
    """
    return render_template('index.html')

@app.route('/register')
def register():
    """
    Description: This function is for manual user registeration.
    Parameter: None
    Return: render_template of register.html
    """
    return render_template('register.html')

@app.route('/login')
def login():
    """
    Description: This function is for manual user login.
    Parameter: None
    Return: render_template of login.html
    """
    return render_template('login.html')
 
@app.route('/google_login')
def google_login():
    """
    Description: This function is creating API for logic of google login via Oauth.
    Parameter: None
    Return: render_template of success.html upon successfull login
    """
    try:
        # Assume the user is logged in so get the user_info
        resp = google.get('/oauth2/v2/userinfo')
        
    except:
        # Ask to google login as the user is not logged in
        return redirect(url_for("google.login"))
    if resp.ok:
        user_info = resp.json()
        access_token = google.token['access_token'] #get the access token generated by google
        username = user_info['id'] #get the id of the user and set it as username 
        real_password = user_info['name'] #get the full name of the user and set it as a unhashed password
        password_hash = sha256_crypt.hash(real_password) #hashing the password
        email = user_info['email']
        full_name = user_info['name']
        user_already_exists = db.session.query(User).filter(User.username==username).one_or_none() #Checking if user already exists
        if not user_already_exists:
            user = User(username, password_hash, email)
            db.session.add(user)
            db.session.commit()
    
    return render_template('success.html',data=f"Hello {full_name} ", token_id = f"{access_token}")

@app.route('/submit_register', methods=['POST'])
def submit_register():
    """
    Description: This function is creating API for logic of manual user registration.
    Parameter: None
    Return: render_template of success.html upon successfull registration
    """
    username = request.form['username']
    real_password = request.form['password_hash']
    password_hash = sha256_crypt.hash(real_password)
    email = request.form['email']

    # Validate email format using regex
    if not re.match(r'^[\w\.-]+@[\w\.-]+$', email):
        return render_template('failure.html', data="Invalid email format")

    if username == "" or real_password == "" or email == "":
        return render_template('failure.html', data="Please check the details you have entered")
    user_exists = db.session.query(User).filter(User.username==username).one_or_none()
    if not user_exists:
        user = User(username, password_hash, email)
        db.session.add(user)
        db.session.commit()
        token = jwt_handler.jwt_encode({"user_id" : user.id})
    
    return render_template('success.html', data=username, token_id=token)


@app.route('/submit_login', methods=['POST'])
def submit_login():
    """
    Description: This function is creating API for logic of manual user login
    Parameter: None
    Return: render_template of success.html upon successfull login
    """
    username=request.form['username']
    real_password=request.form['password_hash'] #Fetching the original password
    if username == "" or real_password == "": #if username or password is blank
        return render_template('failure.html', data="Please check the details you have entered")
    user_exists = db.session.query(User).filter(User.username==username).one_or_none()
    if not user_exists or not sha256_crypt.verify(real_password,user_exists.password_hash): #if user doesn't or wrong password
        return render_template('failure.html', data="You have entered invalid credentials")
    if user_exists and sha256_crypt.verify(real_password,user_exists.password_hash):#generate jwt if all good
        token = jwt_handler.jwt_encode({"user_id" : user_exists.id})
        return render_template('success.html',token_id=token, data=user_exists.username)
    else:
        return render_template('failure.html', data="You have entered invalid credentials")

if __name__ == "__main__":
    app.run(ssl_context='adhoc', debug=True)
