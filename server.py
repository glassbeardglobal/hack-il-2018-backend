from flask import Flask, request, abort, jsonify, g
import api
import time
import copy
app = Flask(__name__)


def verify_keys(d):
    # city, duration, categories, dates, budget
    for item in ['city', 'duration', 'interests', 'date', 'budget']:
        if(item not in d.keys()):
            return None
    return d['city'], d['duration'], d['interests'], d['date'], d['budget']


@app.route('/', methods=['GET', 'POST'])
def index():
    if(request.method == 'GET'):
        return jsonify(getattr(g, 'data', None))
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
        time.sleep(10)
        g.data = copy.deepcopy(t)
        return jsonify(t)


@app.route('/experiences', methods=['GET'])
def experiences():
    arg = request.args.to_dict()


if __name__ == '__main__':
    app.run(debug=True)
