from flask import Blueprint, jsonify, request

from currency_api.data.connectors import exchange_connectors


currency_blueprint = Blueprint('currency', __name__, url_prefix='/exchangeRates')


@currency_blueprint.route('<base_currency>', methods=['GET'])
def get_currency_rates(base_currency):
    """ Endpoint for retrieving currency rates. """
    currencies = request.args.get('symbols', default="").split(",")

    # Compute averages.

    sources = []
    rates = {}
    base = None

    for connector in exchange_connectors:
        try:
            result = connector.get_rates(base_currency, currencies)
            for currency, value in result['rates'].items():
                rates.setdefault(currency, []).append(value)  # Add value
            sources.append(result['datasource'])
            base = result['base'].upper()
        except:
            pass  # Silent retrieval of results.

    if base is None:
        return 'Bad requests', 400
    
    return jsonify({
        'datasource': ", ".join(sources),  # Expected output should be string or list? currently doing all sources as single and averaged.
        'base': base,
        'rates': {
            rate: sum(values) / len(values) for rate, values in rates.items()
        }
    })