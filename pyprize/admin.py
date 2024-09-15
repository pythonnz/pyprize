from flask import render_template, Blueprint
from sqlmodel import select, Session

from pyprize.models import Candidate
from pyprize.db import engine

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.get("/")
def index():
    with Session(engine) as session:
        statement = select(Candidate)
        results = session.exec(statement)

        winners = []
        not_awarded = []
        candidates = []

        for candidate in results:
            if candidate.drawn_at is None:
                candidates.append(candidate)
            elif candidate.awarded_prize is False:
                not_awarded.append(candidate)
            else:
                winners.append(candidate)

        context = {
            "awarded": sorted(winners, key=lambda candidate: candidate.drawn_at),
            "not_awarded": sorted(
                not_awarded, key=lambda candidate: candidate.drawn_at
            ),
            "candidates": candidates,
        }

        return render_template("admin/index.html", **context)
