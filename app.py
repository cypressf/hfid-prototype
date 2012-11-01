from flask import Flask, request, redirect, render_template, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from urlparse import urlparse, urljoin
from sqlalchemy.sql.expression import func, select
from sqlalchemy.dialects import postgresql
from sqlalchemy import *
import os
import random
import string


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
    clients = Client.query.all()
    print clients
    Dave = Client("Dave", "Poop")
    db.session.add(Dave)
    a_workout = Rep_Set_Workout("Barbell Squats", Dave)
    another_workout = Time_Length_Workout("Running", Dave)
    db.session.commit()
    return render_template("home.html",clients=clients)

@app.route("/client/<id>")
def client(id):
    client = Client.query.filter_by(id=id).first()
    return render_template("client.html", client=client)

@app.route("/client/<id>/workouts")
def view_all_workouts(id):
    selected_client = Client.query.filter_by(id=id).first()
    return selected_client.workouts()

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    client_picture_uri = db.Column(db.String(256))

    def __init__(self, firstname, lastname, client_picture_uri='img/profile-photo.jpg'):
        self.firstname = firstname
        self.lastname = lastname
        self.client_picture_uri = client_picture_uri

    def __repr__(self):
        return '<Client %r>' % self.firstname

    def workouts(self):
        this_client_id = self.id
        all_time_length_workouts = Time_Length_Workout.query.filter_by(owner_id=this_client_id).all()
        all_rep_set_workouts = Rep_Set_Workout.query.filter_by(owner_id=this_client_id).all()
        workouts = all_time_length_workouts.append(all_rep_set_workouts)


class Workout(object):

    def __init__(self, name,owner):
        self.name = name
        self.owner_id = owner.id

    def __repr__(self):
        return '<Workout %r>' % self.name

class Time_Length_Workout(Workout, db.Model):
    """
    represents a workout that is measured through distance
    and time. This workout does not implement sets and reps
    """
    __tablename__ = 'time_length_workout'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    time = db.Column(postgresql.FLOAT)
    length = db.Column(postgresql.INTERVAL)

    def __repr__(self):
        return '<Run %r>' % self.name

class Rep_Set_Workout(Workout, db.Model):
    """
    represents a workout that is measured through sets and reps.
    Does not incorporate distance or time.
    """
    __tablename__ = 'rep_set_workout'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    sets = db.Column(postgresql.ARRAY(Integer))
    reps = db.Column(postgresql.ARRAY(Integer))
    weights = db.Column(postgresql.ARRAY(postgresql.FLOAT))

    def __repr__(self):
        return '<rep_set_workout` %r>' % self.name


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)