from flask import Flask, request, abort, jsonify, g, session
from flask_cors import CORS, cross_origin
import os
import api
import time

app = Flask(__name__)
CORS(app)


def verify_keys(d):
    for item in ['city', 'duration', 'interests', 'date', 'budget']:
        if(item not in d.keys()):
            return None
    return d['city'], d['duration'], d['interests'], d['date'], d['budget']


@app.before_request
@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def index():
    if(request.method == 'GET'):
        return jsonify(session.get('data', None))
    elif(request.method == 'OPTIONS'):
        return jsonify({'status': 'ok'}), 200
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
        return jsonify(t)


app.run(debug=True)
