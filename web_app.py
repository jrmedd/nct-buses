"""
Scrapes realtime NCTX bustimes and returns
a JSON object.
"""
from datetime import datetime, timedelta, tzinfo
from math import exp
import os
from flask import Flask, jsonify, session
from flask_cors import CORS
from gazpacho import get, Soup
import requests

APP = Flask(__name__, static_folder='./frontend', static_url_path='/')
APP.secret_key = os.environ.get('SECRET_KEY')
cors = CORS(APP)
STOP_URL = "https://www.nctx.co.uk/stops/%s"

DARK_SKY_KEY = os.environ.get('DARK_SKY_KEY')
DARK_SKY_URL = "https://api.darksky.net/forecast/%s/%s,%s"

TRANSPORT_APP = os.environ.get('TRANSPORT_APP')
TRANSPORT_KEY = os.environ.get('TRANSPORT_KEY')
TRANSPORT_URL = """http://transportapi.com/v3/uk/places.json?
    query=%s&type=bus_stop&app_id=%s&app_key=%s"""


@APP.route('/')
def index():
    """
    Built from the React UI (see in README)
    takes a query string:
    ?stop='ATCOCODE'
    """
    return APP.send_static_file('index.html')


@APP.route('/times/<stopid>')
def times(stopid=None):
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
        due = soup.find(
            'div', {'class': 'single-visit__time--'}, partial=True)
        buses = []
        if len(numbers) == len(destinations) == len(due):
            for i, bus in enumerate(numbers):
                buses.append(
                    {'number': numbers[i].text,
                     'destination': destinations[i].text,
                     'due': due[i].text})
        return jsonify(buses=buses[0:5])

    except Exception:
        return jsonify(buses=[])


@APP.route('/weather/<stopid>')
def weather(stopid=None):
    """
    Uses transport API to get lat/lon
    cooridnates for a bus based on its
    ATCO code. Then gets the daily forecast
    for that location and the current
    temperature, wind speed and bearing.
    """
    now = datetime.now()
    cached = session.get(stopid, {'expiry': now - timedelta(hours=24)})
    now = now.replace(tzinfo=None)
    expiry = cached.get('expiry').replace(tzinfo=None)
    if now > expiry:
      new_expiry = now + timedelta(hours=24)
      bus_stop_request = requests.get(
          TRANSPORT_URL % (stopid, TRANSPORT_APP, TRANSPORT_KEY))
      if bus_stop_request.status_code == 200:
          stop = bus_stop_request.json().get('member')[0]
          lat = stop.get('latitude')
          lon = stop.get('longitude')
          cached.update({'lat': lat, 'lon': lon, 'expiry': new_expiry})
          session.update({stopid: cached})
      else:
        return "Unable to locate bus stop"
    lat = cached.get('lat')
    lon = cached.get('lon')
    print(session)
    if lat and lon:
      weather_request = requests.get(DARK_SKY_URL % (DARK_SKY_KEY, lat, lon))
      if weather_request.status_code == 200:
          forecast = weather_request.json().get('daily').get('summary')
          temperature = (weather_request.json().get(
              'currently').get('temperature')-32)*(5/9)
          wind_speed = (weather_request.json().get(
              'currently').get('windSpeed'))
          wind_bearing = weather_request.json().get(
              'currently').get('windBearing')
          return jsonify(forecast=forecast,
                          temperature=temperature,
                          windSpeed=wind_speed,
                          windBearing=wind_bearing)
      else:
        return "Unable to find weather"
   


if __name__ == '__main__':
    APP.run(host="0.0.0.0", debug=True)
