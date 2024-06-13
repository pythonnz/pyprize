import json
import os

from pathlib import Path
from typing import List, Dict, Optional, Union, Set

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlmodel import Field, SQLModel, create_engine, Session, select, delete
from sqlalchemy.sql import func


app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")


class Candidate(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    already_won: bool = Field(default=False)


def find_pretix_data() -> Path:
    root_dir = Path(__file__).resolve().parent.parent
    files = os.listdir(root_dir)
    for f in files:
        print(f)
        if f.endswith("_pretixdata.json"):
            return Path(f"{root_dir}/{f}")
    raise FileNotFoundError("Could not find pretixdata.json in root of repository.")


def load_orders(path: Path) -> List[Dict]:
    orders = []
    with open(path, "r") as f:
        orders = json.load(f)["event"]["orders"]
    return orders


def get_names_from_orders(orders: List[Dict]) -> List[str]:
    names = []
    for order in orders:
        for position in order["positions"]:
            if position["attendee_name"] is not None:
                names.append(position["attendee_name"])
    return names


def get_names() -> Set[str]:
    try:
        pretix_data_path = find_pretix_data()
        orders = load_orders(pretix_data_path)
        return set(get_names_from_orders(orders))
    except FileNotFoundError:
        with open(CSV_NAME, "r") as csvfile:
            reader = csv.reader(csvfile)
            return set(reader)


def delete_all():
    with Session(engine) as session:
        session.exec(delete(Candidate))
        session.commit()


def import_all():
    names = get_names()
    with Session(engine) as session:
        session.add_all([Candidate(name=name) for name in names])
        session.commit()


@app.get("/reset", response_class=HTMLResponse)
def refresh_table():
    delete_all()
    import_all()
    return "Successfully updated database of candidates"


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    templates = Jinja2Templates(directory="app/templates")
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": TITLE,
            "theme": THEME,
        }
    )


@app.get("/next", response_class=HTMLResponse)
async def get_next(request: Request) -> Union[str | None]:
    with Session(engine) as session:
        query = (
            select(Candidate)
            .where(Candidate.already_won == False)
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

@app.get("/clear")
async def wipe_table():
    delete_all()
    return "Just wiped database of candidates"


TITLE = os.environ.get("TITLE", "Kiwi PyCon XIII 2024")
DB_NAME = os.environ.get("DB_NAME", "candidates.db")
CSV_NAME = os.environ.get("CSV_NAME", "candidates.csv")
PRETIX_EXPORT = os.environ.get("PRETIX_EXPORT", "2024_pretixdata.json")
THEME = {
    "name": "KiwiPyCon2024",
    "favicon": "https://images.squarespace-cdn.com/content/628a8ae9fe38b23ef951d7ef/1d24ee2f-fa7c-4ae6-adf8-2b628f702eb8/kiwi-pycon-xiii-favicon.png?format=100w&content-type=image%2Fpng",
    "logo": "https://images.squarespace-cdn.com/content/v1/628a8ae9fe38b23ef951d7ef/d5339dfd-f142-4d42-9a69-7d7bf97959fa/kiwi-pycon-xiii-logo.png?format=2500w",
}

sqlite_url = f"sqlite:///{DB_NAME}"
engine = create_engine(sqlite_url, echo=True)
SQLModel.metadata.create_all(engine)
