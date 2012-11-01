from flask import Flask, request, redirect, render_template, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from urlparse import urlparse, urljoin
from sqlalchemy.sql.expression import func, select
from sqlalchemy.dialects import postgresql
from sqlalchemy import *
import os
import random
import string
import datetime

#################
# Globals
#################
all_workouts = ['Arm Pullover','Chest Fly','Chest Press','Crossover Chest Fly','Decline Chest Fly','Decline Chest Press','Decline Push Up','Incline Chest Fly','Incline Chest Press','Kneeling Single-Arm Chest Fly','Parallel Grip Chest Press','Reverse Grip Chest Press','Reverse Grip Decline Chest Press','Reverse Grip Incline Chest Press','Single Arm Chest Fly','Single Arm Chest Press','Wide Chest Press','Abdominal Crunch','Cable Abdominal Crunch','Cross-body Pull Over Crunch','Incline Sit-Up','Kneeling Torso Twist','Reverse Fly','Shoulder Abduction','Shoulder Shrug','Supine Cross-Body Shoulder ','Forearm Curl','Incline Biceps Curl','Kneeling Biceps Curl','Kneeling Lateral Biceps Curl','Kneeling Reverse Biceps Curl','Lateral Biceps Curl','Preacher Concentration Curl','Preacher Curl','Preacher Reverse Curl','Prone Biceps Curl','Reverse Forearm Curl','Seated Biceps Curl','Seated Concentration Curl','Seated Reverse Biceps Curl','Supine Biceps Curl','Supine Concentration Curl','Supine Reverse Biceps Curl','High Crossover Lat Row','High Lat Row','Kneeling Lat Row','Lat Fly','Lat Pull-Down','Lat Row','Low Back Extension','Low Crossover Lat Row','Parallel Grip Kneeling Lat Row','Parallel Grip Lat Pull-Down','Parallel Grip Lat Row','Pull Up','Reverse Grip Kneeling Lat Row','Reverse Grip Lat Pull-Down','Reverse Grip Lat Row','Reverse Grip Pull Up','Single Arm Lat Row','Single Arm Pull Up','Surfer Lat Pull','Buns-Up Leg Press','Calf Raise','Cardio Pull','Decline Lunge','Hamstring Curl','Hip Abduction','Hip Adduction','Hip Extension','Incline Lunge','Lateral Lunge','Leg Extension','Leg Thrust','Lying Hip Adduction','Plyometric Split Squat','Plyometric Squat','Rowing Machine','Single Leg Calf Raise','Single Leg Side Squat','Skiing','Split Squat','Sprint Squat','Squat','Standing Split Squat','Toes In Squat','Toes Out Squat','Swimmer','Upright Row','Close Grip Chest Press','Kneeling Reverse Triceps Kickback','Kneeling Triceps Kickback','Lateral Triceps Extension','Overhead Triceps Press','Reverse Grip Overhead Triceps','Reverse Grip Triceps Pressdown','Triceps Dip','Triceps Pressdown']
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
    newguy = Client.query.filter_by(id=8)

    return render_template("home.html",clients=clients)

@app.route("/client/<id>")
def client(id):
    client = Client.query.filter_by(id=id).first()
    return render_template("client.html", client=client)

@app.route("/client/<id>/workouts/<edit>")
def workouts(id, edit):
    if edit == "edit":
        edit = False
    else:
        edit = True

    client = Client.query.filter_by(id=id).first()
    workouts  = client.workouts()
    return render_template("workouts.html",client=client, workouts=workouts, all_workouts=all_workouts, edit=edit)


# api
@app.route("/api/client/<id>/add_workout", methods=['POST'])
def api_add_workout(id):
    client = Client.query.filter_by(id=id).first()
    workout_name = request.form['workout_name']
    workout_type = request.form['workout_type']
    if workout_type == 'time_length_workout':
        new_workout = Time_Length_Workout(workout_name,client)
        new_workout.time = request.form['workout_time']
        new_workout.length = request.form['workout_length']
    elif workout_type == 'rep_set_workout':
        new_workout.reps = request.form['reps']
        new_workout.sets = request.form['sets']
        new_workout.weights = request.form['weights']
    else:
        pass
    new_workout.date = datetime.now()
    db.session.add(new_workout)
    db.session.commit()
    return 'true'

@app.route("/api/client/<id>/workout/<wo_id>/edit", methods=['POST'])
def edit_workout(id,wo_id):
    workout_type_flag = wo_id[0]
    workout_id = wo_id[1:]
    if workout_type_flag == 'r':
        workout = Rep_Set_Workout.query.filter_by(id=workout_id)
        reps = request.form['reps']
        sets = request.form['sets']
        weights = request.form['weights']
        workout.update({
            'reps' : reps,
            'sets' : sets,
            'weigts' : weights
            })
    elif workout_type_flag == 't':
        workout = Time_Length_Workout.query.filter_by(id=workout_id)
        time = request.form['workout_time']
        length = request.form['workout_length']
        workout.update({
            'time' : time,
            'length' : length
            })
    else:
        pass
    db.session.commit()
    return 'true'


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
        all_workouts = []
        all_workouts = all_time_length_workouts + all_rep_set_workouts
        #return sorted(all_workouts, key=lambda x: datetime.datetime.strptime(x.date, '%m/%d/%Y'))
        return all_workouts


class Time_Length_Workout(db.Model):
    """
    represents a workout that is measured through distance
    and time. This workout does not implement sets and reps
    """
    __tablename__ = 'time_length_workout'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    owner_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    time = db.Column(postgresql.FLOAT)
    length = db.Column(postgresql.INTERVAL)
    date = db.Column(db.DateTime)

    def __init__(self, name,owner):
        self.name = name
        self.owner_id = owner.id
        self.date = datetime.now()

    def __repr__(self):
        return '<Time_Length_Workout %r>' % self.name

class Rep_Set_Workout(db.Model):
    """
    represents a workout that is measured through sets and reps.
    Does not incorporate distance or time.
    """
    __tablename__ = 'rep_set_workout'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    owner_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    sets = db.Column(postgresql.ARRAY(Integer))
    reps = db.Column(postgresql.ARRAY(Integer))
    weights = db.Column(postgresql.ARRAY(postgresql.FLOAT))
    date = db.Column(db.DateTime)

    def __init__(self, name,owner):
        self.name = name
        self.owner_id = owner.id
        self.date = datetime.now()

    def __repr__(self):
        return '<rep_set_workout %r>' % self.name

class Measurement(db.Model):
    """
    Represents a measurement (e.g. waist circumference)
    """
    __tablename__ = 'measurements'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(256))
    owner_id = db.Column(db.Integer,db.ForeignKey('clients.id'))
    value = db.Column(postgresql.FLOAT)
    unit = db.Column(db.String(100))

    def __init__(self, name,owner):
        self.name = name
        self.owner_id = owner.id

    def __repr__(self):
        return '<Measurement %r>' % self.name



if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)