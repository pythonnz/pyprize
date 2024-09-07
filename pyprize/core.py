import json
from flask import Blueprint, render_template

from sqlmodel import delete, select
from sqlalchemy.sql import func

from pyprize.db import get_db
from pyprize.utils import get_names
from pyprize.models import Candidate

bp = Blueprint("core", __name__, url_prefix="/")


def delete_all():
    with get_db() as session:
        session.exec(delete(Candidate))
        session.commit()


def import_all():
    names = get_names()
    session = get_db()
    session.add_all([Candidate(name=name) for name in names])
    session.commit()


@bp.get("/reset")
def refresh_table():
    delete_all()
    import_all()
    return "Successfully updated database of candidates"


@bp.get("/")
def index():
    template_vars = {}
    return render_template("core/index.html", **template_vars)


@bp.get("/next")
def get_next():
    session = get_db()
    query = (
        select(Candidate)
        .where(Candidate.already_won == False)  # noqa: E712
        .order_by(func.random())
        .limit(1)
    )
    results = session.exec(query)
    winner = results.first()

    if winner:
        # Mark the candidate as having won
        winner.already_won = True
        session.add(winner)
        session.commit()
        return json.dumps({"name": winner.name, "feedback": ""})
    else:
        return json.dumps({"name": "", "feedback": "No winners left"})


@bp.get("/clear")
def wipe_table():
    delete_all()
    return "Just wiped database of candidates"
