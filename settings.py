"""
@Author: Rohan Vetale

@Date: 2024-04-30 12:40

@Last Modified by: Rohan Vetale

@Last Modified time: 2024-04-30 18:50

@Title : Flask app settings module
"""
from dotenv import load_dotenv
from os import getenv

load_dotenv()
DATABASE_NAME = getenv('DATABASE_NAME')
DATABASE_PASSWORD =getenv('DATABASE_PASSWORD')
DATABASE_DIALECT = getenv('DATABASE_DIALECT')
DATABASE_DRIVER = getenv('DATABASE_DRIVER')
DATABASE_USERNAME = getenv('DATABASE_USERNAME')
HOST = getenv('HOST')
DEFAULT_PORT = getenv('DEFAULT_PORT', default='5432')
SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"
SENDER_EMAIL = getenv('SENDER_EMAIL')
SENDER_PASSWORD = getenv('SENDER_PASSWORD')
REDIS_PORT = getenv('REDIS_PORT')
REDIS_URL = getenv('REDIS_URL')
super_key = getenv('super_key')
APP_SECRET_KEY=getenv('APP_SECRET_KEY')
GOOGLE_CLIENT_ID=getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET=getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_SCOPE=getenv('GOOGLE_SCOPE')
SQLALCHEMY_DATABASE_URI=getenv('SQLALCHEMY_DATABASE_URI')