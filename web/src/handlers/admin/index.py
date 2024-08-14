import logging
import re, json
import subprocess

from flask import Blueprint, render_template, request, redirect, make_response
from models import mdb
from handlers.handler import Handler
from core import limiter
from utils import settings
from utils import utils
from flask import session
from datetime import date
from flask_jwt_extended import create_access_token, get_jwt_identity
from flask_jwt_extended import jwt_required
from utils import utils_db
#from utils import multi_db
#from core import app
from datetime import datetime


class CreateClient(Handler):
    
    decorators = [limiter.limit("15/minute")]
    
    def get(self, errors=None):
        # make response let you add header
        
        response = make_response(
            render_template("admin/create-client.html", errors=errors, \
            csrf_token=self.generate_csrf_token(), \
            key_name=settings.CSRF_KEY))
        
        return response
    
    def post(self):

    	valid_pw = request.form.get('password') == ""
        
        code = str(request.form.get('client-code')).upper() # company name or client code, namespace

        email_addr = str(request.form.get('client-username')).lower() # client first admin username
        
        valid_email = utils.valid_email(email_addr)
        
        valid_code = bool(re.match(r"[A-Za-z0-9/_-]+", code))
        
        valid_csrf = self.check_csrf(request.form.get(settings.CSRF_KEY))
        
        if valid_pw and valid_code and valid_csrf and valid_email:
            
            # create client object and put
            if not mdb.Model().is_client_exists(code):
                
                mdb.Model().create_mdb(email=email_addr, namespace=code)
                
                return """Succeed! return to <a href='/'>main page</a> or continue to 
                    <a href='/create-client'>create client</a>"""

        return self.get(errors="Something's wrong.")