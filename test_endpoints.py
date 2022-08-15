from flask import Flask
APP = Flask(__name__)

@APP.route('/transportapi')
def hello():
    return {'member':[{'latitude': '12.3', 'longitude': '45.6'}]}

if __name__ == '__main__':
    APP.run(debug=True, port=5001)