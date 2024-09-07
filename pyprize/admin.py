from flask import render_template, Blueprint
from sqlmodel import select

from pyprize.models import Candidate
from pyprize.db import get_db

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.get("/")
def index():
    context = {}
    return render_template("admin/index.html", **context)


@bp.get("/winners")
def get_all_winners():
    session = get_db()
    query = select(Candidate).where(Candidate.already_won == True)  # noqa
    winners = [winner.name for winner in session.exec(query).all()]
    return winners
