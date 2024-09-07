import json
from flask import Blueprint, render_template
from sqlmodel import delete, select, Session
from sqlalchemy.sql import func

from pyprize.db import engine
from pyprize.utils import get_names
from pyprize.models import Candidate


bp = Blueprint("core", __name__, url_prefix="/")


def delete_all():
    with Session(engine) as session:
        session.exec(delete(Candidate))
        session.commit()


def import_all():
    names = get_names()
    with Session(engine) as session:
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
    with Session(engine) as session:
        query = (
            select(Candidate)
            .where(Candidate.drawn_at == None)  # noqa: E711
            .order_by(func.random())
            .limit(1)
        )
        results = session.exec(query)
        winner = results.first()

        if winner:
            winner.mark_as_drawn()
            session.add(winner)
            session.commit()
            return json.dumps({"name": winner.name, "feedback": ""})
        else:
            return json.dumps({"name": "", "feedback": "No winners left"})


@bp.get("/clear")
def wipe_table():
    delete_all()
    return "Just wiped database of candidates"
