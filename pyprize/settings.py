import os
from dotenv import load_dotenv

load_dotenv()

TITLE = os.environ.get("PYPRIZE_TITLE", "Kiwi PyCon XIII | 2024")

DB_NAME = os.environ.get("PYPRIZE_DB_NAME", "candidates.db")

CSV_NAME = os.environ.get("PYPRIZE_CSV_NAME", "candidates.csv")

PRETIX_EXPORT = os.environ.get("PYPRIZE_PRETIX_EXPORT", "2024_pretixdata.json")

SECRET_KEY = os.environ.get("PYPRIZE_SECRET_KEY", "this_is_not_secure")

THEME = {
    "name": "KiwiPyCon2024",
    "favicon": "/static/themes/KiwiPyCon2024/favicon.png",
    "logo": "/static/themes/KiwiPyCon2024/kiwi-pycon-xiii-logo.png",
}
