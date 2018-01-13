# -*- coding: utf-8 -*-

import logging
logging.basicConfig(level=logging.DEBUG)

from datetime import datetime, timedelta
import json
from urllib import urlopen
import re

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for, jsonify
from flask import g

from google.appengine.ext import ndb
from google.appengine.api.mail import send_mail
from google.appengine.api import users

app = Flask(__name__)
app.config['DEBUG'] = True


class Word(ndb.Expando):
    name = ndb.StringProperty()
    binary = ndb.StringProperty()
    decimal = ndb.IntegerProperty()
    trending = ndb.IntegerProperty()
    sentiment = ndb.IntegerProperty()

    @classmethod
    def get_words(cls):
        words = [{
                    "name": w.name,
                    "binary": w.binary,
                    "decimal": w.decimal,
                    "length": w.length,
                    "sentiment": w.sentiment,
                 }
                 for w in cls.query().order(Word.name).fetch(10000)]
        return words

class UserModel(ndb.Expando):
    email = ndb.StringProperty()
    abilities = ndb.StringProperty(repeated=True)
    api_key = ndb.StringProperty()
    
    @classmethod
    def get_model(cls, user):
        model = None
        if user:
            model = cls.get_by_id(user.email())
            if model:
                return model
            model = cls(id=user.email())
            model.email = user.email()
            model.put()
            return model
        model = cls(id="guest@example.com")
        model.email = "guest@example.com"
        return model
        
@app.before_request
def my_before_request():
    g.user = users.get_current_user()
    g.user_model = UserModel.get_model(g.user)
    if g.user:
        g.logout_url = users.create_logout_url('/')
    else:
        g.login_url = users.create_login_url('/')

@app.context_processor
def my_ctx():
    return {"g": g, "json": json}

#-- decorators

def needs_api_key(f):
    def decorated_function(*args, **kwargs):
        api_key = request.args.get("api_key")
        if api_key:
            user = UserModel.query(UserModel.api_key == api_key).get()
            if user:
                return f(*args, **kwargs)        
        return jsonify({"status": "error", "message": "bad api key"})
    return decorated_function

#-- api
@app.route('/api/import/<model>/<id>', methods=["GET", "POST"])
@needs_api_key
def api_import(model, id):
    Model = globals().get(model)
    if not Model:
        return jsonify({"status": "error", "message": "bad model"})

    obj = Model.get_by_id(id)
    if not obj:
        obj = Model(id=id)
    
    for k, v in json.loads(request.get_data()).items():
        setattr(obj, k, v)
        
    obj.put()

    return jsonify({"result": obj._to_dict()})

@app.route('/api/words')
def api_words():
    return jsonify({"result": Word.get_words()})


#-- views
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.errorhandler(404)
def page_not_found(e):
    return '404 No mnemonics here.', 404

