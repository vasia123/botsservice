import json
from functools import wraps

import flask

from exceptions import Unauthorized
from inventories import parse_inv
from steambots import SteamBots


with open('valid_api_keys') as file:
    valid_api_keys = [line.strip() for line in file]
bots = SteamBots()


app = flask.Flask(__name__)


@app.errorhandler(Unauthorized)
def handle_invalid_usage(error):
    response = flask.jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def validate_apikey(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        req_key = flask.request.headers.get('x-api-key')
        if not any(req_key == s for s in valid_api_keys):
            raise Unauthorized('Unauthorized', 401)
        return f(*args, **kwargs)

    return decorated_function


@app.route('/api/account')
@validate_apikey
def get_bots():
    return str(bots)


@app.route('/api/trade/inventory')
# @validate_apikey
def get_inv():
    steam_ids = flask.request.args.get('steamID')
    # app_id = flask.request.args.get('appID')

    inventories = parse_inv(*steam_ids.split(','))

    return json.dumps(inventories)


@app.route('/api/trade')
@validate_apikey
def make_tradeoffer():
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0')
