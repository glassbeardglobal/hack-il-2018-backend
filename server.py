from flask import Flask, request, abort, jsonify, g, session
import os
import api
import time
import pyrebase

config = {
    "apiKey": "AIzaSyBc3ZW1iEOZxBv6QhvMn8cm8QySEJo5Ov0",
    "authDomain": "hackillinois-amadeus-2018.firebaseapp.com",
    "databaseURL": "https://hackillinois-amadeus-2018.firebaseio.com",
    "storageBucket": "hackillinois-amadeus-2018.appspot.com"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

app = Flask(__name__)


def verify_keys(d):
    for item in ['city', 'duration', 'interests', 'date', 'budget']:
        if(item not in d.keys()):
            return None
    return d['city'], d['duration'], d['interests'], d['date'], d['budget']


@app.before_request
@app.route('/', methods=['GET', 'POST'])
def index():
    if(request.method == 'GET'):
        return jsonify(session['data'])
    else:
        args = request.get_json()
        items = verify_keys(args)
        if(items is None):
            abort(400)
        city, duration, interests, date, budget = items
        duration = int(duration)
        budget = int(budget)
        date = time.strftime("%m-%d-%Y", time.localtime(date)).split('-')
        date[0], date[1], date[2] = date[2], date[0], date[1]
        date = '-'.join(date)
        t = api.main(city, budget, interests, date, duration)
        session['data'] = t
        db.child('data').set(t)
        time.sleep(2)
        return jsonify(t)


app.secret_key = os.urandom(24)
app.run(debug=True)
