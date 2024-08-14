import logging
import re

from flask import Blueprint, render_template, request, redirect, make_response
from flask_jwt_extended import create_access_token
from models import client_model
from models import user_model
from handlers.handler import Handler
from core import limiter
from utils import settings
from utils import utils
from flask import session


class IndexPage(Handler):
    
    decorators = [limiter.limit("20/minute")]
    " url: /"
    def get(self):
        
        logging.info(request.headers)
        
        response = make_response(render_template("index.html"))
        
        return response
    
    def post(self):
        pass