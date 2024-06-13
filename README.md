# pyPrize

Simple prize draw generator for displaying at a conference etc. Runs as a local web app.

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Download the name list from pretix in JSON format and place in the root of the directory

```
https://pretix.eu/control/event/${organisation}/${short_event_name}/orders/export/?identifier=json
```

E.g. https://pretix.eu/control/event/kiwipycon/2024/orders/export/?identifier=json

Start the server

```bash
fastapi dev app/main.py
```

Open your browser to http://localhost:8000/

## TODO:

 * [ ] Update design
 * [ ] Parameterise color palette for easy, branded reuse between KPCs
 * [ ] Restore database functionality for persistent state between process restarts
