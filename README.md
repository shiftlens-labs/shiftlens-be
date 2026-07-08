# ShiftLens BE

Flask REST API for manufacturing shift handoff cards, alert ingest, shift board, and audit trail.

## Local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app.main run --port 5001
pytest
```

Quick syntax smoke check without installing dependencies:

```bash
python -m compileall app tests
```

## REST API

- `POST /api/v1/auth/signin`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/logout`
- `GET /api/v1/shifts/current`
- `GET /api/v1/handoff-cards?shiftId=&status=`
- `GET /api/v1/handoff-cards/<id>`
- `PATCH /api/v1/handoff-cards/<id>`
- `POST /api/v1/handoff-cards/<id>/actions`
- `GET /api/v1/alerts`
- `POST /api/v1/alerts/ingest`

## Architecture

```text
app/
  main.py
  modules/
    auth/
    alerts/
    handoff/
    shifts/
    audit/
  db/models.py
```

The API uses an in-memory repository for local portfolio verification. `app/db/models.py` defines the PostgreSQL/TimescaleDB-oriented Tortoise ORM shape: relational shift/card/action tables plus `AlertEvent.time` for hypertable-style TSDB storage.

Skipped: real migrations and DB boot. Add Aerich + TimescaleDB container when persistence matters.
