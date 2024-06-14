# pyprize

Simple prize draw generator for displaying at a conference etc. Runs as a local web app.

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Get data and place it in the root of the pyprize repo. See the section below for detailed information about getting data. E.g.

```bash
cp candidates.csv.example candidates.csv
```

Start the server

```bash
fastapi dev app/main.py
```

Open your browser to http://localhost:8000/

## Usage

Click 'Fresh Import' to reset set the initial state of the database with the data from the filesystem

Click the `Draw Winner` button to draw a new winner. You can also press `spacebar` or `enter`.

Click the `Clear` to reset ready for the next prize draw. You can also press `spacebar` or `enter`.

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
ruff check .
ruff format .
```
