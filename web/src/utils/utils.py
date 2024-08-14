# -*- coding: utf-8 -*-

import os, re, time
import hmac
import logging
import datetime
import hashlib
import random, string


SECRET = ""
REQUEST_RE = ""
SECURE_KEY = ""

#RE
PHONE_RE = re.compile(r"^[0-9]{8}$")
PASS_RE = re.compile(r"^.{3,20}$")
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
EMAIL_RE  = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
COOKIE_RE = re.compile(r'.+=;\s*Path=/')


def timeit(method):
    "time the functions"
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        logging.info("%r (%r, %r) %2.7f" % (method.__name__, args, kw, ts-te))
        return result
    return timed

def valid_month(month):
	if month[:3].capitalize() in months:
		return month.capitalize()
	return None

def valid_day(day):
	if day and day.isdigit():
		day = int(day)
		if day > 0 and day <= 31:
			return day
	return None

def valid_year(year):
	if year and year.isdigit():
		year = int(year)
		if year >= 1900 and year <= 2020:
			return year
	return None	

def convert_category_from_url(cat_url):
	return cat_url.replace("_", " ").title()

def escape_html(s):
	for (i, o) in (("&", "&amp;"),
	                   (">", "&gt;"),
	                   ("<", "&lt;"),
	                   ('"', "&quot;")):
		s = s.replace(i, o)
	return s

def valid_username(username):
	return username and USER_RE.match(username)

def valid_password(password):
	return password and PASS_RE.match(password)

def valid_email(email):
	return email and EMAIL_RE.match(email)

def valid_phone_number(phone_number):
	return phone_number and PHONE_RE.match(phone_number)

def valid_cookie(cookie):
	return cookie and COOKIE_RE.match(cookie)

def hash_str(s):
	return hmac.new(SECRET.encode("utf-8"), s.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()

def make_secure_val(s):
	return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
	val = h.split("|")[0]
	if make_secure_val(val) == h:
		return val
	else:
		return None

def make_salt(length=10):
	return ''.join(random.choice(string.ascii_letters) for i in range(length))

"""
replaced by bcrypt
def make_pw_hash(name, pw, salt = None):
	# The constant SECRET is pepper. 
	
	if not salt:
		salt = make_salt()
	hash_str = name + pw + salt+ str(SECRET)
	h = hashlib.sha256(hash_str.encode('utf-8')).hexdigest()
	return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
	salt = h.split(',')[0]
	return h == make_pw_hash(name, password, salt)
"""
