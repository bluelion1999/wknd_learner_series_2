# Inventory API

[![CI](https://github.com/bluelion1999/wknd_learner_series_2/actions/workflows/ci.yml/badge.svg)](https://github.com/bluelion1999/wknd_learner_series_2/actions/workflows/ci.yml)

A small but complete REST API for managing inventory items and the categories they belong to. Built with FastAPI and PostgreSQL, containerized end to end, with schema migrations and a full test suite.

Built as a weekend learning project — the commit history walks from a single `hello world` endpoint to what's here now, one concept at a time.

## Stack

| | |
|---|---|
| **FastAPI** | routing, request/response validation, auto-generated OpenAPI docs |
| **PostgreSQL 16** | persistence, referential integrity, constraint enforcement |
| **SQLAlchemy 2.0** | ORM, using the modern `DeclarativeBase` / `Mapped` / `select()` style |
| **Alembic** | versioned schema migrations |
| **Pydantic v2** | input validation and response serialization |
| **pytest** | 37 tests against a real Postgres database |
| **Docker Compose** | one command to run the whole stack |

## Quick start

Requires Docker. No local Python or Postgres install needed.

```bash
cp .env.example .env          # then edit the credentials
docker compose up --build -d
docker compose exec api alembic upgrade head
```

The API is at **http://127.0.0.1:8000**, interactive docs at **http://127.0.0.1:8000/docs**.

## API

### Items

| Method | Path | Description |
|---|---|---|
| `GET` | `/items` | List items. Supports `?skip=` and `?limit=` |
| `GET` | `/items/{item_id}` | Fetch one item |
| `POST` | `/items` | Create an item |
| `PUT` | `/items/{item_id}` | Replace an item's fields |
| `DELETE` | `/items/{item_id}` | Delete an item |

### Categories

| Method | Path | Description |
|---|---|---|
| `GET` | `/categories` | List categories. Supports `?skip=` and `?limit=` |
| `GET` | `/categories/{category_id}` | Fetch one category |
| `POST` | `/categories` | Create a category |
| `PUT` | `/categories/{category_id}` | Replace a category's fields |
| `DELETE` | `/categories/{category_id}` | Delete a category, if no items reference it |

### Example

```bash
curl -X POST http://127.0.0.1:8000/categories \
  -H "Content-Type: application/json" \
  -d '{"name": "stationery", "description": "desk supplies"}'

curl -X POST http://127.0.0.1:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "pen", "price": 5.0, "category_id": 1}'
```

Items embed their category rather than making the client fetch it separately:

```json
{
  "id": 1,
  "name": "pen",
  "price": 5.0,
  "category_id": 1,
  "category": {
    "id": 1,
    "name": "stationery",
    "description": "desk supplies",
    "created_at": "2026-08-02T19:11:39.746351Z"
  },
  "in_stock": true,
  "created_at": "2026-08-02T19:11:39.813555Z"
}
```

### Status codes

| Code | Meaning |
|---|---|
| `200` | Success |
| `400` | Referenced a resource that doesn't exist (e.g. an unknown `category_id`) |
| `404` | The requested resource doesn't exist |
| `409` | Conflicts with current state — duplicate category name, or deleting a category that still has items |
| `422` | Request body or query params failed validation |

## Validation rules

- `price` must be greater than zero
- `name` is required, 1–100 characters, and may not be blank or whitespace-only
- Leading and trailing whitespace on names is stripped before storage
- Category names are unique, enforced by the database
- `skip` must be ≥ 0; `limit` must be between 1 and 100

## Project structure

```
app/
  main.py            FastAPI app, router wiring, global exception handlers
  database.py        engine, session factory, Base, get_db dependency
  models.py          SQLAlchemy models (ItemDB, CategoryDB)
  schemas.py         Pydantic request/response schemas
  dependencies.py    shared dependencies (pagination)
  routers/
    items.py         /items endpoints
    categories.py    /categories endpoints
alembic/             migrations
tests/               pytest suite
```

Models describe the database; schemas describe the API. They're deliberately separate — the two diverge as soon as the database stores something the API shouldn't expose.

## Tests

```bash
docker compose exec api pytest
```

Tests run against a dedicated `apidb_test` database, not your development data. Each test starts with empty tables and drops them afterward, so tests are isolated and order-independent.

The `get_db` dependency is swapped for a test session via FastAPI's `dependency_overrides`, which is the reason endpoints declare `db: Session = Depends(get_db)` rather than opening sessions inline.

Postgres is used for tests rather than SQLite deliberately: constraint behavior is a large part of what's being tested, and SQLite doesn't enforce foreign keys the same way.

## Migrations

The schema is owned by Alembic, not by `create_all()`. After changing a model:

```bash
docker compose exec api alembic revision --autogenerate -m "describe the change"
# read the generated file before applying it
docker compose exec api alembic upgrade head
```

Useful commands:

```bash
docker compose exec api alembic check          # is a migration missing?
docker compose exec api alembic downgrade -1   # roll back one migration
docker compose exec api alembic history        # list migrations
```

Run migrations *before* deploying code that depends on them — new code against an old schema fails on every request.

## Design notes

**Deleting a category with items is refused, not cascaded.** The relationship uses `passive_deletes=True` so SQLAlchemy doesn't quietly null out the children's `category_id`; the database's foreign key fires instead and the API returns `409`. Reassign or delete the items first. Silently orphaning rows is the kind of data loss nobody notices until much later.

**List endpoints are ordered and bounded.** `OFFSET`/`LIMIT` without `ORDER BY` gives no stable pagination — rows can shift between queries, so pages may repeat or skip records. Both list endpoints order by `id`, and `limit` is capped at 100.

**Related data is eager-loaded.** Serializing a nested category per item would issue one query per row (the N+1 problem). `selectinload` fetches them in a single additional query, so the query count doesn't grow with the result size.

**Integrity errors are handled centrally, with local overrides.** A global handler maps Postgres error codes to HTTP status — `23505` to `409`, `23503` to `400`. Routes that can give a more specific message, like category deletion, catch the error themselves; the global handler is the fallback.

**Credentials come from the environment.** Nothing sensitive is committed — see `.env.example` for the required variables.

## CI

Every push to `main` and every pull request runs migrations from an empty database, verifies models match migrations with `alembic check`, and runs the full test suite against Postgres.
