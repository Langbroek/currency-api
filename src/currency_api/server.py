
from flask import Flask

from waitress import serve

from dao.blueprints import currency_blueprint, metrics_blueprint


# Init the application
def create_currency_exchange_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='r4ndoms3cretkey',
    )
    # Disable key sorting
    try:
        app.config['JSON_SORT_KEYS'] = False
        app.json.sort_keys = False
    except:
        pass
    # Max size allowed is 150mb.
    app.config['MAX_CONTENT_LENGTH'] = 150 * 1000 * 1000

    # Register all the blue prints
    app.register_blueprint(currency_blueprint)
    app.register_blueprint(metrics_blueprint)

    return app


# Create and run the app
def main():
    app = create_currency_exchange_app()
    serve(app, host="localhost", port=5000)


if __name__ == '__main__':
    main()
