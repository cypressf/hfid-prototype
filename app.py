from flask import Flask, request, redirect, render_template, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from urlparse import urlparse, urljoin
from sqlalchemy.sql.expression import func, select
from sqlalchemy.dialects import postgresql
from sqlalchemy import *
import os
import random
import string
from datetime import date, datetime

#################
# Globals
#################
all_workouts = [('Arm Pullover','Time_Length_Workout'),('Chest Fly','Time_Length_Workout'),('Chest Press','Time_Length_Workout'),('Crossover Chest Fly','Time_Length_Workout'),('Decline Chest Fly','Time_Length_Workout'),('Decline Chest Press','Time_Length_Workout'),('Decline Push Up','Time_Length_Workout'),('Incline Chest Fly','Time_Length_Workout'),('Incline Chest Press','Time_Length_Workout'),('Kneeling Single-Arm Chest Fly','Time_Length_Workout'),('Parallel Grip Chest Press','Time_Length_Workout'),('Reverse Grip Chest Press','Time_Length_Workout'),('Reverse Grip Decline Chest Press','Time_Length_Workout'),('Reverse Grip Incline Chest Press','Time_Length_Workout'),('Single Arm Chest Fly','Time_Length_Workout'),('Single Arm Chest Press','Time_Length_Workout'),('Wide Chest Press','Time_Length_Workout'),('Abdominal Crunch','Time_Length_Workout'),('Cable Abdominal Crunch','Time_Length_Workout'),('Cross-body Pull Over Crunch','Time_Length_Workout'),('Incline Sit-Up','Time_Length_Workout'),('Kneeling Torso Twist','Time_Length_Workout'),('Reverse Fly','Time_Length_Workout'),('Shoulder Abduction','Time_Length_Workout'),('Shoulder Shrug','Time_Length_Workout'),('Supine Cross-Body Shoulder ','Time_Length_Workout'),('Forearm Curl','Time_Length_Workout'),('Incline Biceps Curl','Time_Length_Workout'),('Kneeling Biceps Curl','Time_Length_Workout'),('Kneeling Lateral Biceps Curl','Time_Length_Workout'),('Kneeling Reverse Biceps Curl','Time_Length_Workout'),('Lateral Biceps Curl','Time_Length_Workout'),('Preacher Concentration Curl','Time_Length_Workout'),('Preacher Curl','Time_Length_Workout'),('Preacher Reverse Curl','Time_Length_Workout'),('Prone Biceps Curl','Time_Length_Workout'),('Reverse Forearm Curl','Time_Length_Workout'),('Seated Biceps Curl','Time_Length_Workout'),('Seated Concentration Curl','Time_Length_Workout'),('Seated Reverse Biceps Curl','Time_Length_Workout'),('Supine Biceps Curl','Time_Length_Workout'),('Supine Concentration Curl','Time_Length_Workout'),('Supine Reverse Biceps Curl','Time_Length_Workout'),('High Crossover Lat Row','Time_Length_Workout'),('High Lat Row','Time_Length_Workout'),('Kneeling Lat Row','Time_Length_Workout'),('Lat Fly','Time_Length_Workout'),('Lat Pull-Down','Time_Length_Workout'),('Lat Row','Time_Length_Workout'),('Low Back Extension','Rep_Set_Workout'),('Low Crossover Lat Row','Rep_Set_Workout'),('Parallel Grip Kneeling Lat Row','Rep_Set_Workout'),('Parallel Grip Lat Pull-Down','Rep_Set_Workout'),('Parallel Grip Lat Row','Rep_Set_Workout'),('Pull Up','Rep_Set_Workout'),('Reverse Grip Kneeling Lat Row','Rep_Set_Workout'),('Reverse Grip Lat Pull-Down','Rep_Set_Workout'),('Reverse Grip Lat Row','Rep_Set_Workout'),('Reverse Grip Pull Up','Rep_Set_Workout'),('Single Arm Lat Row','Rep_Set_Workout'),('Single Arm Pull Up','Rep_Set_Workout'),('Surfer Lat Pull','Rep_Set_Workout'),('Buns-Up Leg Press','Rep_Set_Workout'),('Calf Raise','Rep_Set_Workout'),('Cardio Pull','Rep_Set_Workout'),('Decline Lunge','Rep_Set_Workout'),('Hamstring Curl','Rep_Set_Workout'),('Hip Abduction','Rep_Set_Workout'),('Hip Adduction','Rep_Set_Workout'),('Hip Extension','Rep_Set_Workout'),('Incline Lunge','Rep_Set_Workout'),('Lateral Lunge','Rep_Set_Workout'),('Leg Extension','Rep_Set_Workout'),('Leg Thrust','Rep_Set_Workout'),('Lying Hip Adduction','Rep_Set_Workout'),('Plyometric Split Squat','Rep_Set_Workout'),('Plyometric Squat','Rep_Set_Workout'),('Rowing Machine','Rep_Set_Workout'),('Single Leg Calf Raise','Rep_Set_Workout'),('Single Leg Side Squat','Rep_Set_Workout'),('Skiing','Rep_Set_Workout'),('Split Squat','Rep_Set_Workout'),('Sprint Squat','Rep_Set_Workout'),('Squat','Rep_Set_Workout'),('Standing Split Squat','Rep_Set_Workout'),('Toes In Squat','Rep_Set_Workout'),('Toes Out Squat','Rep_Set_Workout'),('Swimmer','Rep_Set_Workout'),('Upright Row','Rep_Set_Workout'),('Close Grip Chest Press','Rep_Set_Workout'),('Kneeling Reverse Triceps Kickback','Rep_Set_Workout'),('Kneeling Triceps Kickback','Rep_Set_Workout'),('Lateral Triceps Extension','Rep_Set_Workout'),('Overhead Triceps Press','Rep_Set_Workout'),('Reverse Grip Overhead Triceps','Rep_Set_Workout'),('Reverse Grip Triceps Pressdown','Rep_Set_Workout'),('Triceps Dip','Rep_Set_Workout'),('Triceps Pressdown','Rep_Set_Workout')]
stock_measurements = [('Weight','lbs'),('Arms','in'),('Forearms','in'),('Neck','in'),('Chest','in'),('Waist','in'),('Thighs','in'),('Calves','in')]
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
    return render_template("home.html",clients=clients)

@app.route("/client/<id>")
def client(id):
    client = Client.query.filter_by(id=id).first()
    return render_template("client.html", client=client)

@app.route("/client/<id>/workouts/<edit>")
def workouts(id, edit):
    if edit == "edit":
        edit = True
    else:
        edit = False
    client = Client.query.filter_by(id=id).first()
    top_workouts  = client.top_workouts()
    all_workouts_sorted = sorted(all_workouts,key=lambda x: x[0])
    return render_template("workouts.html",client=client, workouts=top_workouts, all_workouts=all_workouts_sorted, edit=edit)

# api
@app.route("/api/client/<id>/add_workout", methods=['POST'])
def api_add_workout(id):
    client = Client.query.filter_by(id=id).first()
    workout_name = request.form['workout_name']
    workout_type = request.form['workout_type']
    if workout_type == 'Time_Length_Workout':
        new_workout = Time_Length_Workout(workout_name,client)
        new_workout.time = request.form['workout_time']
        new_workout.length = request.form['workout_length']
    if workout_type == 'Rep_Set_Workout':
        new_workout = Rep_Set_Workout(workout_name,client)
        new_workout.reps = [int(x) for x in request.form['reps'].split(',')]
        new_workout.sets = request.form['sets']
        new_workout.weights = [float(x) for x in request.form['weights'].split(',')]
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
            'weights' : weights
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
        return sorted(all_workouts, key=lambda x: x.date)

    def top_workouts(self):
        this_client_id = self.id
        counts_time_length_workouts = db.session.query(func.count(Time_Length_Workout.id),Time_Length_Workout.name).group_by(Time_Length_Workout.name).all()
        counts_rep_set_workouts = db.session.query(func.count(Rep_Set_Workout.id),Rep_Set_Workout.name).group_by(Rep_Set_Workout.name).all()
        counts_workouts = counts_time_length_workouts + counts_rep_set_workouts
        top_workouts = sorted(counts_workouts, key=lambda x: x[0])
        return top_workouts[0:3]  

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
    sets = db.Column(db.Integer)
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

def random_date():
    start_date = date.today().replace(day=1, month=1).toordinal()
    end_date = date.today().toordinal()
    random_day = date.fromordinal(random.randint(start_date, end_date))
    return random_day

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)