# import sqlite3
import click
from flask import g
from sqlmodel import create_engine, Session

from pyprize import settings


def get_db():
    if "db" not in g:
        # db_url = current_app.config["DATABASE"]
        db_url = f"sqlite:///{settings.DB_NAME}"

        engine = create_engine(db_url, echo=True)
        g.db = Session(engine)

    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    pass
    # db_url = current_app.config["DATABASE"]
    # engine = create_engine(db_url, echo=True)
    # db = get_db()
    # with current_app.open_resource("schema.sql") as f:
    #     db.executescript(f.read().decode("utf8"))


@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
