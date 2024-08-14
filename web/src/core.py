
import logging 
import socketio
from datetime import timedelta

from flask import Flask
from flask_limiter import Limiter
from flask_cors import CORS
from flask_limiter.util import get_remote_address
from utils import settings
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from celery import Celery
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# All app configs and settings
app.config['DEBUG'] = settings.DEBUG
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = settings.DB_URI.format("test")
app.secret_key = settings.SESSION_KEY
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)

# https://flask-jwt-extended.readthedocs.io/en/stable/token_locations/
app.config['JWT_SECRET_KEY'] = settings.JWT_SECRET_KEY
app.config['JWT_ALGORITHM'] = 'HS256'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=8)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
app.config["JWT_COOKIE_SECURE"] = False
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config["JWT_COOKIE_CSRF_PROTECT"] = False
app.config['CORS_HEADERS'] = 'Content-Type'


if settings.DEBUG: 
    logging.basicConfig(filename='../logs/error.log', level=logging.DEBUG)


#db = SQLAlchemy(app)

# flask-limiter
limiter = Limiter(app, key_func=get_remote_address, 
                  default_limits=["2000/day", "750/hour", "150/minute"])

# flask jwt
jwt = JWTManager(app)

celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"]) #

celery.conf.update(app.config)