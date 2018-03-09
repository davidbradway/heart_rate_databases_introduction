import datetime

from pymodm import connect
from pymodm import MongoModel, fields

from flask import Flask, jsonify, request
app = Flask(__name__)

connect("mongodb://localhost:27017/bme590") # connect to database

class HeartRate(MongoModel):
    user_email = fields.EmailField(primary_key=True),
    user_age = fields.IntegerField(),
    heart_rate = fields.FloatField(),
    time = fields.DateTimeField()

@app.route("/api/heart_rate", methods=["POST"])
def set_heart_rate():
    r = request.get_json() # parses the POST request body as JSON
    hr = HeartRate(user_email=r["user_email"],
                   user_age=r["user_age"],
                   heart_rate=r["heart_rate"],
                   time=datetime.datetime.now())
    hr.save()
    return jsonify({"Result": "saved"}), 200

def helper_get_by_email(user_email):
    """
    Queries and returns all HearRate objects by given user_email
    """
    return HeartRate.objects.raw({"user_email": user_email})

@app.route("/api/heart_rate/<user_email>", methods=["GET"])
def get_by_email(user_email):
    """
    Should return all heart rate measurements for that user
    """
    heartrates = helper_get_by_email(user_email)
    return jsonify(heartrates), 200

@app.route("/api/heart_rate/average/<user_email>", methods=["GET"])
def get_average_by_email(user_email):
    """
    Should return the user's average heart rate over all measurements
    """
    heartrates = helper_get_by_email(user_email)
    total: float = 0.0
    count: int = 0
    for entry in heartrates:
        total += entry.heart_rate
        count += 1
    if count != 0:
        return jsonify({"average": total/count}), 200
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

    total: float = 0.0
    count: int = 0
    for entry in HeartRates.objects.raw({"user_email":user_email, "time": {'$gte': since}}):
        total += entry.heart_rate
        count += 1

    # TODO determine tachycardia for user_age

    if count != 0:
        return jsonify({"average": total/count}), 200
    else:
        return jsonify({"error": "no entries"}), 400

