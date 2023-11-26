import importlib.metadata

from flask import Flask, g
from logging.config import dictConfig

# Import Bootstrap Budget modules
from . import accounts
from . import admin
from . import auth
from . import budget
from . import budget_items
from . import config
from . import dashboard
from . import db
from . import transactions
from . import users


# Set Bootstrap Budget version
__version__: str = importlib.metadata.version("bootstrap_budget")


dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


def main() -> Flask:
    """
    The main function for Bootstrap Budget.

    :return: A Flask app (Bootstrap Budget)
    """
    # Create and configure the app
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    # Register Bootstrap Budget blueprints
    app.register_blueprint(accounts.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(budget.bp)
    app.register_blueprint(budget_items.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(transactions.bp)
    app.register_blueprint(users.bp)

    # Define the index entry point: The Boostrap Budget Dashboard
    app.add_url_rule("/", endpoint="dashboard.index")

    return app
