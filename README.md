# Music Store — Profile Service

Profile management microservice for the **Music Store** project, responsible for creating and querying customers and staff members.

---

## Stack

| Layer      | Technology                           |
| ---------- | ------------------------------------ |
| Language   | Python 3.13                          |
| Framework  | Django 6.0                           |
| API        | Django REST Framework 3.17           |
| Auth       | djangorestframework-simplejwt 5.5.1  |
| OpenAPI    | drf-spectacular + sidecar            |
| Linter     | Ruff 0.16                            |
| Templates  | djHTML / djLint                      |
| Container  | Docker / Docker Compose              |

---

## Data Model

```
Profile (abstract)
├── uuid          (UUID, PK)
├── user_uuid     (UUID, unique)
├── first_name    (string, 100)
├── last_name     (string, 100)
├── doc           (string, 11, unique)
├── address       (string, 250)
├── address_number (string, 10, nullable)
├── address_line_2 (string, 250, nullable)
├── neighborhood  (string, 250)
├── city          (string, 250)
├── state         (string, 2)
├── country       (string, 3)
├── created_at    (datetime, auto_now_add)
└── updated_at    (datetime, auto_now)

Customer(Profile)          Staff(Profile)
                           ├── staff_id (integer, 7, unique)
                           └── role     (string, 50)
```

Both concrete models use **custom managers** (`CustomerManager`, `StaffManager`) that apply input sanitization via `ProfileValidationService` (strip whitespace, alphanumeric validation) before persisting. Each profile is linked to an auth-service user via the `user_uuid` field, which is read-only and set automatically on creation from the JWT token.

---

## Environment-specific Settings

The project uses three settings modules extending `config/settings/base.py`:

| Environment | File                      | Database         | `DJANGO_SETTINGS_MODULE`        |
| ----------- | ------------------------- | ---------------- | ------------------------------- |
| Development | `config/settings/dev.py`  | SQLite           | `config.settings.dev` (default) |
| Production  | `config/settings/prod.py` | PostgreSQL       | `config.settings.prod`          |
| Testing     | `config/settings/test.py` | In-memory SQLite | `config.settings.test`          |

**Required environment variables:**

- `DEV_PROJECT_KEY` — Django secret key (all environments)
- Production: `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` (optional), `DB_PORT` (optional), `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`

---

## Local Development

```bash
# Clone the repository
git clone https://github.com/orgjr/music-store-profile-service.git
cd music-store-profile-service

# Create and activate virtualenv
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver
```

The API will be available at `http://localhost:8000`.

---

## Running Tests

```bash
python manage.py test tests --settings=config.settings.test --verbosity=2
```

The test suite has **206 tests** covering unit (models, managers, validation service), functional (serializers), and endpoint (full HTTP requests) layers.

---

## Project Structure

```
config/                         # Django project configuration
├── settings/
│   ├── base.py                 # Shared settings (apps, REST, spectacular, JWT)
│   ├── dev.py                  # SQLite, debug
│   ├── prod.py                 # PostgreSQL, production hardening
│   └── test.py                 # In-memory SQLite

core/                           # Core app — service info + health
├── exceptions.py               # Custom API exceptions
├── views.py                    # index/health endpoints
└── urls.py

profiles/                       # Profiles app
├── base/
│   └── models.py               # Profile (abstract base + user_uuid)
├── customer/
│   ├── models.py               # Customer(Profile)
│   ├── manager.py              # CustomerManager (validation on create)
│   ├── serializers.py          # CustomerSerializer
│   ├── views.py                # CustomerViewSet (JWT, per-action permissions)
│   └── urls.py                 # SimpleRouter → customers/
├── staff/
│   ├── models.py               # Staff(Profile) + StaffId field
│   ├── manager.py              # StaffManager (staff_id/role + profile validation)
│   ├── serializers.py          # StaffSerializer
│   ├── views.py                # StaffViewSet (JWT, staff-only)
│   └── urls.py                 # SimpleRouter → staffs/
├── validators/                   # Input validators
│   ├── __init__.py              # Exports validate_alphanumeric, validate_doc
│   ├── alphanumeric.py          # validate_alphanumeric(attr, value)
│   └── doc.py                   # validate_doc(value)
├── services/
│   ├── validation.py            # ProfileValidationService
│   └── request.py               # Request helpers (placeholder)
├── permissions.py               # IsOwner, IsStaff, IsOwnerOrStaff
├── migrations/                  # Database migrations
└── urls.py                     # Aggregator — includes customer/ and staff/ urls

docs/                           # OpenAPI schema annotations (drf-spectacular)
└── api/
    ├── index.py                # Service info endpoint schema
    ├── health.py               # Health check endpoint schema
    └── profiles/
        ├── __init__.py         # Exports customers_schema, staffs_schema
        ├── config.py           # Shared examples, helpers, response builders
        ├── customers.py        # Customer CRUD schemas
        └── staffs.py           # Staff CRUD schemas

schema.yml                      # Generated OpenAPI 3.0.3 schema

tests/                          # Centralized test suite
├── core/
│   ├── test_index.py           # 9 tests
│   └── test_health.py          # 8 tests
└── profiles/
    ├── base/
    │   ├── test_models.py      # 7 tests
    │   └── test_validation.py  # 23 tests
    ├── customer/
    │   ├── test_models.py      # 21 tests
    │   ├── test_serializers.py # 29 tests
    │   └── test_endpoints.py   # 31 tests
    └── staff/
        ├── test_models.py      # 13 tests
        ├── test_serializers.py # 20 tests
        ├── test_endpoints.py   # 27 tests
        └── test_staff_id.py    # 18 tests
```

---

## Endpoints

All profile endpoints require a **JWT Bearer token** (`Authorization: Bearer <token>`).
Core endpoints accept optional authentication.

### Core

| Method | Route             | Description                       |
| ------ | ----------------- | --------------------------------- |
| GET    | `/api/v1/`        | Service metadata (name, version…) |
| GET    | `/api/v1/health/` | Health check (status, uptime)     |

### Profiles — Customers

| Method | Route                                     | Description                                       | Auth            |
| ------ | ----------------------------------------- | ------------------------------------------------- | --------------- |
| GET    | `/api/v1/profiles/customers/`             | List all customers (newest first)                 | Staff           |
| POST   | `/api/v1/profiles/customers/`             | Create a customer (`user_uuid` from JWT)          | Authenticated   |
| GET    | `/api/v1/profiles/customers/{uuid}/`      | Retrieve a customer                              | Owner or Staff  |
| PUT    | `/api/v1/profiles/customers/{uuid}/`      | Replace a customer (all fields)                  | Owner or Staff  |
| PATCH  | `/api/v1/profiles/customers/{uuid}/`      | Partially update a customer                      | Owner or Staff  |
| DELETE | `/api/v1/profiles/customers/{uuid}/`      | Delete a customer                                | Staff           |

### Profiles — Staff

| Method | Route                                     | Description                                       | Auth   |
| ------ | ----------------------------------------- | ------------------------------------------------- | ------ |
| GET    | `/api/v1/profiles/staffs/`               | List all staff members (newest first)             | Staff  |
| POST   | `/api/v1/profiles/staffs/`               | Create a staff member (`user_uuid` from JWT)      | Staff  |
| GET    | `/api/v1/profiles/staffs/{uuid}/`        | Retrieve a staff member                          | Staff  |
| PUT    | `/api/v1/profiles/staffs/{uuid}/`        | Replace a staff member (all fields)              | Staff  |
| PATCH  | `/api/v1/profiles/staffs/{uuid}/`        | Partially update a staff member                  | Staff  |
| DELETE | `/api/v1/profiles/staffs/{uuid}/`        | Delete a staff member                            | Staff  |

### OpenAPI Documentation

| Tool    | URL               |
| ------- | ----------------- |
| Schema  | `/api/v1/schema/` |
| Swagger | `/api/v1/docs/`   |
| Redoc   | `/api/v1/redoc/`  |

---

## Deploy with Docker / Docker Compose

### Build and run

```bash
cd ./music-store-profile-service
docker compose -f compose.yaml up --build
```

The container exposes port `8000` and mounts the current directory as a volume at `/app`, enabling hot-reload during development.

### Production (example with `compose.prod.yaml`)

```yaml
services:
  web:
    build: .
    ports:
      - '8000:8000'
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.prod
      - DEV_PROJECT_KEY=<secret>
      - DB_NAME=musicstore
      - DB_USER=musicstore
      - DB_PASSWORD=<password>
      - DB_HOST=db
      - ALLOWED_HOSTS=mydomain.com
      - CSRF_TRUSTED_ORIGINS=https://mydomain.com
    depends_on:
      - db

  db:
    image: postgres:16
    environment:
      POSTGRES_DB: musicstore
      POSTGRES_USER: musicstore
      POSTGRES_PASSWORD: <password>
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

> **Note:** In production, set up a reverse proxy (nginx/Caddy) and use an async WSGI server (gunicorn/uwsgi) instead of `runserver`.

---

## Planned Improvements

- [x] Authentication and authorization (JWT via simplejwt)
- [ ] CI/CD with GitHub Actions
- [x] Health check and observability enhancements
- [ ] Database migrations squashing
- [ ] Rate limiting and throttling
- [x] Adapt endpoint tests to new routes and JWT authentication
- [ ] Implement self-profile endpoint (`me/`) with `get_queryset()` lookup by `user_uuid`
