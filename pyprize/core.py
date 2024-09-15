from flask import Blueprint, render_template, jsonify, request
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

        winner_json = winner.model_dump()

        if winner:
            winner.mark_as_drawn()
            session.add(winner)
            session.commit()
            return jsonify({"candidate": winner_json, "feedback": ""})
        else:
            return jsonify({"candidate": "", "feedback": "No winners left"})


@bp.post("/candidate/<int:candidate_id>/award")
def award(candidate_id: int):
    award_prize = request.json.get("award_prize", False)

    with Session(engine) as session:
        query = (
            select(Candidate).where(Candidate.id == candidate_id)  # noqa: E711
        )
        results = session.exec(query)
        candidate = results.first()

        if award_prize:
            candidate.awarded_prize = True

        session.add(candidate)
        session.commit()

    return ("OK", 200)


@bp.get("/clear")
def wipe_table():
    delete_all()
    return "Just wiped database of candidates"
