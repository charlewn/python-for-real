# -*- coding: utf-8 -*-

import logging
import pickle
import json
import bcrypt
from datetime import datetime
from core import db
from models import nsql
from utils import utils


class Client(db.Model, nsql.Model):
    
    __tablename__ = "Client"
    
    id = db.Column('client_id', db.BigInteger , primary_key=True)
    
    client_code = db.Column('client_code', db.String(10), unique=True)
    
    # password = db.Column('password', db.String(100))
    # start of client settings
    lang = db.Column('lang', db.String(4), default='EN')
     
    created = db.Column('created' , db.DateTime, default=datetime.now())
    
    updated = db.Column('updated' , db.DateTime, default=datetime.now(), onupdate=datetime.now())
    
    def __init__(self, client_code):
        self.client_code = client_code
        # self.password = password
        
    def __repr__(self):
        return '<Client %r>' % (self.client_code)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "client_code": self.client_code,
            "created": self.created,
            "updated": self.updated
        }
    
    @classmethod
    def get_by_code(cls, code):
        """
        Get client by client code
        :params: code, client code; 
        :return: client object
        """
        return Client.query.filter(Client.client_code==code).first()
    
    @classmethod
    def get_by_id(cls, client_id):
        return Client.query.filter(Client.id==client_id).first()
    
    @classmethod
    def is_exists(cls, code):
        "Check if client exists"
        client = cls.get_by_code(code)
        return True if client is not None else False
    
    """
    @classmethod
    def login_by_code(cls, client_code, pw):
        c = cls.get_by_code(client_code)
        if c and cls.valid_pw(client_code, pw):
            return c, c.client_code
        else:
            return None, None
    
    @classmethod
    def valid_pw(cls, name, pw):
        c = cls.get_by_code(name)
        if not c: return False
        hash_str = name + pw + str(utils.SECRET)
        return bcrypt.checkpw(hash_str.encode('utf-8'), c.password.encode('utf-8'))
    
    @classmethod
    def make_pw_hash(cls, name, pw, salt = None):
        if not salt:
            salt = bcrypt.gensalt(12)
        hash_str = name + pw + str(utils.SECRET)
        h = bcrypt.hashpw(hash_str.encode('utf-8'), salt)
        return h
    """