from heart_rate_databases_starter import models
from heart_rate_databases_starter import main
import datetime

from pymodm import connect
from pymodm import MongoModel, fields

from flask import Flask, jsonify, request
app = Flask(__name__)

connect("mongodb://localhost:27017/heart_rate_app") # connect to database

@app.route("/api/heart_rate", methods=["POST"])
def set_heart_rate():
    r = request.get_json() # parses the POST request body as JSON

    user = helper_get_by_email(r["user_email"])
    print(user)
    print(type(user))

    if user is None:
        # create a new Users instance
        u = heart_rate_databases_starter.models.User(email=r["user_email"],
                                                     age=r["user_age"],
                                                     heart_rate=[],
                                                     heart_rate_times=[]) 
    u.heart_rate.append(r["heart_rate"])
    u.heart_rate_times.append(datetime.datetime.now())
    u.save()
    return jsonify({"result": "saved"}), 200

def helper_get_by_email(user_email):
    """
    Queries and returns all HearRate objects by given user_email
    """
    user = heart_rate_databases_starter.models.User.objects.raw({"_id": user_email}).first() # Get the first user where _id=email
    return user

def helper_get_users_average_heart_rate(user):
    if len(user.heart_rate) > 0:
        avg: float = sum(user.heart_rate)/len(user.heart_rate)
    else:
        avg = None
    return avg

@app.route("/api/heart_rate/<user_email>", methods=["GET"])
def get_by_email(user_email):
    """
    Should return all heart rate measurements for that user
    """
    user = helper_get_by_email(user_email)
    return jsonify(user.heart_rate), 200

@app.route("/api/heart_rate/average/<user_email>", methods=["GET"])
def get_average_by_email(user_email):
    """
    Should return the user's average heart rate over all measurements
    """
    user = helper_get_by_email(user_email)
    avg = helper_get_users_average_heart_rate(user)
    if avg is not None:
        return jsonify({"average": avg}), 200
    else:
        return jsonify({"error": "no entries"}), 400

@app.route("/api/heart_rate/interval_average", methods=["POST"])
def get_average_by_email_since():
    """
    Should calculate and return the average heart rate for the user since the
    time specified. This should also return an indication of weather this
    average heart rate is considered tachycardic for the user's current (latest
    recorded) age.
    """
    r = request.get_json() # parses the POST request body as JSON
    user_email = r["user_email"]
    heart_rate_average_since = r["heart_rate_average_since"] #"2018-03-09 11:00:36.372339" // date string
    since = datetime.strptime(heart_rate_average_since, "%Y-%m-%d %H:%M:%S.%f")

    # TODO determine tachycardia for user_age

    user =  heart_rate_databases_starter.models.User.objects.raw({"user_email":user_email, "time": {'$gte': since}}).first()
    avg = helper_get_users_average_heart_rate(user)
    if avg is not none:
        return jsonify({"average": avg}), 200
    else:
        return jsonify({"error": "no entries"}), 400

