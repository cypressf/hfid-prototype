from flask import Flask, request, redirect, render_template, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from urlparse import urlparse, urljoin
import uuid
from sqlalchemy.sql.expression import func, select
from sqlalchemy.dialects import postgresql
from sqlalchemy import *
import os
import random
import string
import uuid


#################
# Globals
#################
app = Flask(__name__)
try:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['HEROKU_POSTGRESQL_SILVER_URL']
except Exception, e:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://gtfomqcakbtbjc:PqNH-Ltth50qTb6V63gkUJt7uV@ec2-107-21-107-221.compute-1.amazonaws.com:5432/d2n3c81nka07du'
db = SQLAlchemy(app)
metadata = MetaData()

@app.route("/")
def home():
    Dave = Client('Dave','Poop')
    print Dave
    db.session.add(Dave)
    db.session.commit()
    myrun = Time_Length_Workout('myfirstrun',Dave)
    print myrun
    db.session.add(myrun)
    db.session.commit()
    return render_template("home.html")

@app.route("/client/<id>")
def client(id):
    return render_template("client.html", id=id)

@app.route("/dave")
def dave():
    return render_template("dave.html")


class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.String(256), primary_key=True)
    firstname = db.Column(db.String(100), unique=True)
    lastname = db.Column(db.String(100), unique=True)

    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname
        self.id = uuid.uuid4().hex

    def __repr__(self):
        return '<Client %r>' % self.firstname

class Workout(object):

    def __init__(self, name,owner):
        self.name = name
        self.owner_id = owner.id
        self.id = uuid.uuid4().hex

    def __repr__(self):
        return '<Workout %r>' % self.name

class Time_Length_Workout(Workout, db.Model):
    """
    represents a workout that is measured through distance
    and time. This workout does not implement sets and reps
    """
    __tablename__ = 'time_length_workout'
    id = db.Column(db.String(256), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    time = db.Column(postgresql.FLOAT)
    length = db.Column(postgresql.INTERVAL)
    # owner = db.relationship('Client')

    def __repr__(self):
        return '<Run %r>' % self.name

class WeightLifting(Workout, db.Model):
    """
    represents a workout that is measured through sets and reps.
    Does not incorporate distance or time.
    """
    __tablename__ = 'WeightLifting'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    sets = db.Column(postgresql.ARRAY(Integer))
    reps = db.Column(postgresql.ARRAY(Integer))
    weights = db.Column(postgresql.ARRAY(postgresql.FLOAT))
    # owner = db.relationship('Client')



    def __repr__(self):
        return '<WeightLifting %r>' % self.name


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)