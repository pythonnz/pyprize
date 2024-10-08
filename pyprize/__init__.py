import os
from flask import Flask

from pyprize import settings
from pyprize import admin
from pyprize import auth
from pyprize import core

from pyprize.db import create_db_and_tables
from pyprize.models import Candidate  # noqa: F401


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=settings.SECRET_KEY,
        DATABASE=os.path.join(app.instance_path, "pyprize.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    create_db_and_tables()

    app.register_blueprint(core.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)

    @app.context_processor
    def inject_variables():
        return dict(theme=settings.THEME, title=settings.TITLE)

    return app
