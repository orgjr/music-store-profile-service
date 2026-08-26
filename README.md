# Music Store — Profile Service

Profile management microservice for the **Music Store** project, responsible for creating and querying customers and staff members.

---

## Stack

| Layer     | Technology                 |
| --------- | -------------------------- |
| Language  | Python 3.13                |
| Framework | Django 6.0                 |
| API       | Django REST Framework 3.17 |
| OpenAPI   | drf-spectacular + sidecar  |
| Linter    | Ruff 0.16                  |
| Templates | djHTML / djLint            |
| Container | Docker / Docker Compose    |

---

## Data Model

```
Profile (abstract)
├── uuid          (UUID, PK)
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
└── created_at    (datetime, auto)

Customer(Profile)          Staff(Profile)
                           ├── staff_id (integer, 7, unique)
                           └── role     (string, 50)
```

Both concrete models use **custom managers** (`CustomerManager`, `StaffManager`) that apply input sanitization via `ProfileValidationService` (strip whitespace, alphanumeric validation) before persisting.

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

The test suite has **191 tests** covering unit (models, managers, validation service), functional (serializers), and endpoint (full HTTP requests) layers.

---

## Project Structure

```
config/                         # Django project configuration
├── settings/
│   ├── base.py                 # Shared settings (apps, REST, spectacular)
│   ├── dev.py                  # SQLite, debug
│   ├── prod.py                 # PostgreSQL, production hardening
│   └── test.py                 # In-memory SQLite

core/                           # Core app — service info + health
├── views.py                    # index/health endpoints
└── urls.py

profiles/                       # Profiles app
├── base/
│   └── models.py               # Profile (abstract base)
├── customer/
│   ├── models.py               # Customer(Profile)
│   ├── manager.py              # CustomerManager (validation on create)
│   └── serializers.py          # CustomerSerializer
├── staff/
│   ├── models.py               # Staff(Profile)
│   ├── manager.py              # StaffManager (staff_id/role + profile validation)
│   └── serializers.py          # StaffSerializer
├── validators/                   # Input validators
│   ├── __init__.py              # Exports validate_alphanumeric, validate_doc
│   ├── alphanumeric.py          # validate_alphanumeric(attr, value)
│   └── doc.py                   # validate_doc(value)
├── services/
│   └── profile_validation.py   # ProfileValidationService
├── views.py                    # CustomerViewSet + StaffViewSet (ModelViewSets)
└── urls.py                     # DefaultRouter registrations

docs/                           # OpenAPI schema annotations (drf-spectacular)
└── api/
    ├── index.py                # Service info endpoint schema
    ├── health.py               # Health check endpoint schema
    └── profiles/
        ├── customer.py         # Customer CRUD schemas
        └── staff.py            # Staff CRUD schemas

tests/                          # Centralized test suite
├── core/
│   ├── test_index.py           # 9 tests
│   └── test_health.py          # 8 tests
└── profiles/
    ├── base/
    │   ├── test_models.py      # 4 tests
    │   └── test_validation.py  # 22 tests
    ├── customer/
    │   ├── test_models.py      # 17 tests
    │   ├── test_serializers.py # 29 tests
    │   └── test_endpoints.py   # 29 tests
    └── staff/
        ├── test_models.py      # 9 tests
        ├── test_serializers.py # 20 tests
        ├── test_endpoints.py   # 26 tests
        └── test_staff_id.py    # 18 tests
```

---

## Endpoints

### Core

| Method | Route             | Description                       |
| ------ | ----------------- | --------------------------------- |
| GET    | `/api/v1/`        | Service metadata (name, version…) |
| GET    | `/api/v1/health/` | Health check (status, uptime)     |

### Customer CRUD

| Method | Route                               | Description                                    |
| ------ | ----------------------------------- | ---------------------------------------------- |
| GET    | `/api/v1/profiles/customer/`        | List (paginated, ordered by `created_at` desc) |
| POST   | `/api/v1/profiles/customer/`        | Create                                         |
| GET    | `/api/v1/profiles/customer/{uuid}/` | Retrieve                                       |
| PUT    | `/api/v1/profiles/customer/{uuid}/` | Full update                                    |
| PATCH  | `/api/v1/profiles/customer/{uuid}/` | Partial update                                 |
| DELETE | `/api/v1/profiles/customer/{uuid}/` | Delete                                         |

### Staff CRUD

| Method | Route                            | Description                                    |
| ------ | -------------------------------- | ---------------------------------------------- |
| GET    | `/api/v1/profiles/staff/`        | List (paginated, ordered by `created_at` desc) |
| POST   | `/api/v1/profiles/staff/`        | Create                                         |
| GET    | `/api/v1/profiles/staff/{uuid}/` | Retrieve                                       |
| PUT    | `/api/v1/profiles/staff/{uuid}/` | Full update                                    |
| PATCH  | `/api/v1/profiles/staff/{uuid}/` | Partial update                                 |
| DELETE | `/api/v1/profiles/staff/{uuid}/` | Delete                                         |

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

- [ ] Authentication and authorization
- [ ] CI/CD with GitHub Actions
- [x] Health check and observability enhancements
- [ ] Database migrations squashing
- [ ] Rate limiting and throttling
