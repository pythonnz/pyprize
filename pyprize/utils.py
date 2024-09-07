import json
import os
import csv

from pathlib import Path
from typing import List, Dict, Set

from pyprize import settings


def find_pretix_data() -> Path:
    root_dir = Path(__file__).resolve().parent.parent
    files = os.listdir(root_dir)
    for f in files:
        if f.endswith("_pretixdata.json"):
            return Path(f"{root_dir}/{f}")
    raise FileNotFoundError("Could not find pretixdata.json in root of repository.")  # noqa


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
        pass

    with open(settings.CSV_NAME, "r") as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
        names = set([row[0] for row in rows])
        return names
