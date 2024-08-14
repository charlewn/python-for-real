
# Handler files for login and render all types of extended templates

import jinja2
import os
import logging
import json
import time
import random
import string

from flask import Blueprint, render_template, request, make_response, redirect
from flask.views import MethodView
from flask import session
from utils import settings
from utils import utils
from flask_jwt_extended import jwt_required



class Handler(MethodView):
    """The base handler class"""
        
    def render_str(self, template, **params):
        # t = jinja_env.get_template("maintenance.html") # uncomment for maintenance 
        t = jinja_env.get_template(template)

        return t.render(params)
    
    def render(self, template, **kw):
        #self.write(self.render_str("maintenance.html", **kw))
        
        return render_template(template, **kw)
    
    def auth_user(self):
        
        user_cookie = request.cookies.get("username")

        namespace = request.cookies.get('ns', "test")
        
        user_logged_in = False
        
        username = ""
        
        if user_cookie and namespace and utils.check_secure_val_ns(user_cookie, namespace):
            
            username = user_cookie.split('|')[0]
            
            user_logged_in = True

        return username, user_logged_in, namespace

    def generate_csrf_token(self):
        " Generate a csrf token use in form submission "
        if settings.CSRF_KEY not in session:

            session[settings.CSRF_KEY] = self.generate_random_string(length=32)
        
        return session[settings.CSRF_KEY]

    def remove_csrf_token(self):
        session.pop(settings.CSRF_KEY, None)
        
    def generate_random_string(self, length=16):
        " Secure token for CSRF "
        return ''.join(random.choice(string.ascii_uppercase + string.digits) \
               for x in range(length))
    
    def check_csrf(self, token):
        " Check to see if token is valid "
        if settings.CSRF_KEY not in session:
            return False
        if str(session[settings.CSRF_KEY]) == token:
            return True
        else:
            return False