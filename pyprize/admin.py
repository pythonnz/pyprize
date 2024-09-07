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
        candidates = []

        for candidate in results:
            if candidate.drawn_at is None:
                candidates.append(candidate)
            else:
                winners.append(candidate)

        context = {
            "winners": sorted(winners, key=lambda winner: winner.drawn_at),
            "candidates": candidates,
        }

        return render_template("admin/index.html", **context)


# @bp.get("/winners")
# def get_all_winners():
#     with Session(engine) as session:
#         query = select(Candidate).where(Candidate.drawn_at != None)  # noqa: E712 E501
#         winners = [winner.name for winner in session.exec(query).all()]
#         return winners
