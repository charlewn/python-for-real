# -*- coding: utf-8 -*-

import logging
import pickle
import json
import bcrypt
from utils import settings
from datetime import datetime
from core import db
from models import nsql
from utils import utils
# from itsdangerous.serializer import Serializer
# from itsdangerous import TimestampSigner
from itsdangerous.url_safe import URLSafeTimedSerializer
from itsdangerous.exc import SignatureExpired, BadSignature
# 


class User(db.Model, nsql.Model):
    
    __tablename__ = "User"
    
    id = db.Column('user_id', db.BigInteger , primary_key=True)
    
    client_id = db.Column('client_id', db.BigInteger, db.ForeignKey('Client.client_id'))
    
    username = db.Column('username', db.String(20))
    
    password = db.Column('password' , db.String(100))
    
    tmp_salt = db.Column('tmp_salt', db.String(18))
    
    is_admin = db.Column('is_admin', db.Boolean, default=False)
    
    created = db.Column('created' , db.DateTime, default=datetime.now())

    updated = db.Column('updated' , db.DateTime, default=datetime.now(), onupdate=datetime.now())
    
    def __init__(self, username, password, client_id, is_admin):
        self.username = username
        self.password = password
        self.client_id = client_id
        self.is_admin = is_admin
        
    def __repr__(self):
        return '<User %r>' % (self.username)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "created": self.created,
            "updated": self.updated
        }
    
    @classmethod
    def get_by_name(cls, name):
        """
        Get user by username
        :params: name; 
        :return: user object
        """
        return User.query.filter(User.username==name).first()
    
    @classmethod
    def get_by_id(cls, user_id):
        return User.query.filter(User.id==user_id).first()
    
    @classmethod
    def is_exists_by_client_id(cls, name, cid):
        " Check if username exists in client id"
        user = cls.get_by_name(name)
        return True if user.client_id == cid else False
    
    @classmethod
    def is_exists(cls, name):
        "Check if user exists"
        user = cls.get_by_name(name)
        return True if user is not None else False
    
    @classmethod
    def valid_pw(cls, name, pw):
        u = cls.get_by_name(name)
        if not u: return False
        hash_str = name + pw + str(utils.SECRET)
        return bcrypt.checkpw(hash_str.encode('utf-8'), u.password.encode('utf-8'))
    
    @classmethod
    def make_pw_hash(cls, name, pw, salt = None):
        if not salt:
            salt = bcrypt.gensalt(12)
        hash_str = name + pw + str(utils.SECRET)
        h = bcrypt.hashpw(hash_str.encode('utf-8'), salt)
        return h
    
    @classmethod
    def from_doc(cls, doc):
        if doc is None:
            return None
        user = User(doc['id'], 
                    doc['username'], 
                    doc['password'])
        return user
    
    @classmethod
    def authenticate(cls, name, pw):
        # User.query.filter_by(username=username).one_or_none()
        user = User.from_doc(db.users.find_one({"username": name}))
        authenticated = True if user is not None and user.password == pw else False
        return user if authenticated else None
    
    def gen_auth_token(self):
        # generate jws token, default expires in 30 mins 
        self.tmp_salt = utils.make_salt()
        s = URLSafeTimedSerializer(utils.STS_SECRET_KEY, salt=self.tmp_salt)
        return s.dumps({'id': self.id})
    
    def verify_auth_token(self, token, expired=300):
        # verify jws token, 300/60 = 5 mins default
        s = URLSafeTimedSerializer(utils.STS_SECRET_KEY, salt=self.tmp_salt)
        try:
            data = s.loads(token, max_age=expired)
        except SignatureExpired:
            # valid token, but expired
            logging.info("signature expired")
            return None
        except BadSignature:
            logging.info("Bad sign")
            return None # invalid token
        user_id = data['id']
        # user = User.query.get(data['id'])
        return user_id
    
    @classmethod
    def login_by_name(cls, name, pw):
        u = cls.get_by_name(name)
        if u and cls.valid_pw(name, pw):
            return u, u.username
        else:
            return None, None