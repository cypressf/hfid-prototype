from flask import Flask, request, redirect, render_template, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from urlparse import urlparse, urljoin
import uuid
from sqlalchemy.sql.expression import func, select
import os
import random
import string


#################
# Globals
#################
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['HEROKU_POSTGRESQL_SILVER_URL']
db = SQLAlchemy(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/client/<id>")
def client(id):
    return render_template("client.html", id=id)

@app.route("/dave")
def dave():
    return render_template("dave.html")


class Client(db.Model):
    __tablename__ = 'Client'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), unique=True)
    lastname = db.Column(db.String(100), unique=True)

    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

    def __repr__(self):
        return '<Client %r>' % self.firstname

class Workout(db.Model):
    __tablename__='Workout'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    owner = db.relationship('Client')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Workout %r>' % self.name

class Run(Workout):
    _


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)