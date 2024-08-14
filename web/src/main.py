import logging
from datetime import datetime
from datetime import timedelta
from datetime import timezone

from core import app
from core import db
from core import limiter
from core import jwt


from werkzeug.routing import BaseConverter

from handlers.pages import page
from handlers.admin.index import CreateClient

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies
from flask_jwt_extended import get_jwt

from flask import jsonify, request, send_file, make_response, send_from_directory, redirect


app.url_map.converters['regex'] = utils_flask.RegexConverter
app.url_map.converters['list'] = utils_flask.ListConverter

# use blueprint for APIs
app.register_blueprint(apis_v1)

# Adding the page rules, Using Flask Pluggable Views
app.add_url_rule(r'/', view_func=IndexPage.as_view('index'))
app.add_url_rule(r'/create-client', view_func=CreateClient.as_view('admin')) 


limiter.init_app(app) # initializing the limiter

@app.before_request
def befores():
    
    logging.info(request.headers)
    
    if ":" in request.headers["Host"]:
        return "400"
    