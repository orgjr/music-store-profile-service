from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.staticfiles",
    "core",
    "docs",
    "profiles",
    "rest_framework",
    "drf_spectacular",
    "drf_spectacular_sidecar",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
    },
]

WSGI_APPLICATION = "config.wsgi.application"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTStatelessUserAuthentication",
    ),
}

SIMPLE_JWT = {
    "USER_ID_CLAIM": "user_uuid",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Music Store Profile Service",
    "DESCRIPTION": "Profile management microservice for the Music Store project — "
    "responsible for creating and querying customers and staff members.",
    "VERSION": "0.9.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    "TAGS": [
        {
            "name": "Core",
            "description": "Core endpoints — service information and health check.",
        },
        {
            "name": "Customers",
            "description": "Customer endpoints — full CRUD for customer profiles.",
        },
        {
            "name": "Staff",
            "description": "Staff endpoints — full CRUD for staff profiles (staff access only).",
        },
    ],
    "CONTACT": {
        "name": "Osmar Garcia",
        "email": "osmar.rgj@gmail.com",
        "url": "https://github.com/orgjr",
    },
    "LICENSE": {"name": "MIT"},
}
