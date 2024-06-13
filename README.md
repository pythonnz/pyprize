# pyPrize

Simple prize draw generator for displaying at a conference etc. Runs as a local web app.

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Get data and place it in the root of the pyprize repo. See the section below for detailed information about getting data.

```bash
cp candidates.csv.example candidates.csv
```

Start the server

```bash
fastapi dev app/main.py
```

Open your browser to http://localhost:8000/

## Getting data

The app will work from either a JSON export from pretix or text file which is just a list of names.

 1. Will look for `*_pretixdata.json` at the root of pyprize.
 2. Will look for `candidates.csv` or whatever is set for `CSV_NAME` at the root of pyprize.

In either case, the data must be placed in the root of the directory.

### Pretix Data

Download the name list from pretix in JSON format and place in the root of the directory

```
https://pretix.eu/control/event/${organisation}/${short_event_name}/orders/export/?identifier=json
```
E.g. https://pretix.eu/control/event/kiwipycon/2024/orders/export/?identifier=json

The data is structured as follows

```json
{
    "event": {
        // ...
        "orders": [
            {
                "code": "AB1CD",
                // ...
                "positions": [
                    {
                        "id": 12345678,
                        // ...
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

The CSV should not contain a header row

```
John Smith
Jane Doe
German Kaiser
Julius Caesar
```

## Themes

The app is themeable via the `THEMES` global variable and assets under `static/themes/<theme name>`

## Contributing

Pull requests welcome ❤️

See https://github.com/pythonnz/PyPrize/issues for open issues or to raise bugs / feature requests.

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
