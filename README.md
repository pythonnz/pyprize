# pyprize

![Code Style](https://github.com/pythonnz/pyprize/actions/workflows/code-style.yml/badge.svg)
![Dependencies](https://github.com/pythonnz/pyprize/actions/workflows/pip-audit.yml/badge.svg)

Simple prize draw generator for displaying at a conference etc. Runs as a local web app.

This project uses [`uv`](https://docs.astral.sh/uv).

## Quick Start

Get data and place it in the root of the pyprize repo. See the section below for detailed information about getting data. E.g.

```bash
cp candidates.csv.example candidates.csv
```

Start the server

```bash
uv run flask --app pyprize run --debug
```

Open your browser to http://localhost:8000/

### Usage

 * Click ⚙️ to go to the admin page and then click `FRESH IMPORT` to reset set the initial state of the database with the data from the filesystem

 * Click 🏠 to go back to the main screen

 * Draw a user by pressing `spacebar` or `enter` key.

 * Confirm the prize will be awarded by the drawn candidate by pressing the ➡️ or press ⬅️ to reject the prize draw. 'rejected' candidates will be marked has having been drawn but not awarded the prize.

 * Reset the prize draw by clicking ⚙️ then `FRESH IMPORT`. This will drop the existing database and re import from our data source into a fresh database.

### Building and Running with Docker

```bash
docker build -t pyprize .
```

```bash
docker run -p 5000:5000 pyprize
```

```bash
docker run \
  -v "$(pwd)/candidates.csv.example:/app/candidates.csv" \
  -p 5000:5000 \
  pyprize
```

## Getting data

The app will work from either a JSON export of orders from Pretix or a csv file which is just a list of names.

 1. Will first look for `*_pretixdata.json` at the root of pyprize.
 2. Will look for `candidates.csv` or whatever is set for `CSV_NAME` at the root of pyprize.

In either case, the data must be placed in the root of the directory.

### Pretix Data

Download the name list from Pretix in JSON format and place in the root of the directory

Orders > Export > Order data > Order data (JSON)

E.g. https://pretix.eu/control/event/kiwipycon/2024/orders/export/?identifier=json

The data is structured as follows

```json
{
  "event": {
    "orders": [
      {
        "code": "AB1CD",
        "positions": [
          {
            "id": 12345678,
            "attendee_name": "John Smith"
          }
        ]
      }
    ]
  }
}
```

### CSV List of Candidates

Despite expecting a CSV, we only care about a single column containing the names of the people eligible to win a prize.

The CSV should not contain a header row. E.g. `pyprize/candidates.csv` with a contents of.

```
John Smith
Jane Doe
Joe Bloggs
Julius Caesar
```

## Themes

The app is themeable via the `THEMES` global variable and assets under `static/themes/<theme name>`

## Contributing

Pull requests welcome ❤️

See https://github.com/pythonnz/pyprize/issues for open issues or to raise bugs / feature requests.

This repository uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting.

Install development dependencies with

```bash
pip install -r requirements-dev.txt
```

Check and format with ruff

```bash
uv run ruff check .
uv run ruff format .
```
