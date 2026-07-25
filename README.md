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
                           ├── rn    (string, 7)
                           └── role  (string, 50)
```

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

## Deploy with Docker / Docker Compose

### Build and run

```bash
# Build the image
docker compose build

# Start the service
docker compose up -d
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

## Endpoints

| Method | Route                 | Description           |
| ------ | --------------------- | --------------------- |
| POST   | `/profiles/customer/` | Create a customer     |
| POST   | `/profiles/staff/`    | Create a staff member |

OpenAPI documentation available at:

- Swagger UI: `http://localhost:8000/api/schema/swagger-ui/`
- Redoc: `http://localhost:8000/api/schema/redoc/`

---

## Planned Improvements

- [ ] Full CRUD endpoints with serializers and validation
- [ ] Detailed OpenAPI documentation with examples (`@extend_schema`)
- [ ] Automated tests (unit, integration)
- [ ] Authentication and authorization
- [ ] CI/CD with GitHub Actions
- [ ] Health check and observability
