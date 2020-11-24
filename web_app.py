#!/usr/local/bin/python3
"""
Scrapes realtime NCTX bustimes and returns
a JSON object.
"""
import os
from gazpacho import get, Soup
from flask import Flask, jsonify
from flask_cors import CORS


APP = Flask(__name__)
APP.secret_key = os.environ.get('SECRET_KEY')
cors = CORS(APP)
STOP_URL = "https://www.nctx.co.uk/stops/%s"


@APP.route('/stop/<stopid>')
def stop(stopid=None):
    """
    GET request returns the next 5
    bus numbers, destinations, and times.
    Stop IDS available:
    https: // www.nctx.co.uk/open-data/network/current
    """
    try:
        html = get(STOP_URL % (stopid))
        soup = Soup(html)
        numbers = soup.find(
            'p', {'class': 'single-visit__name'}, partial=False)
        destinations = soup.find(
            'p', {'class': 'single-visit__description'}, partial=False)
        times = soup.find(
            'div', {'class': 'single-visit__time--'}, partial=True)
        buses = []
        if len(numbers) == len(destinations) == len(times):
            for i, bus in enumerate(numbers):
                print(bus)
                buses.append(
                    {'number': numbers[i].text,
                     'destination': destinations[i].text,
                     'due': times[i].text})
        return jsonify(buses=buses[0:5])

    except Exception:
        return jsonify(buses=[])


if __name__ == '__main__':
    APP.run(host="0.0.0.0", debug=True)
