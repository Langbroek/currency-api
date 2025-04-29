from flask import Blueprint, jsonify

from currency_api.utils.metrics import api_metrics_to_json


metrics_blueprint = Blueprint('metrics', __name__, url_prefix='/metrics')


@metrics_blueprint.route('', methods=['GET'])
def get_api_metrics():
    """ Endpoint for retrieving currency rates. """

    return jsonify(api_metrics_to_json()), 200
