import os

from config.settings.base import *

ENV = "development"

DEBUG = True

SECRET_KEY = os.environ["DEV_PROJECT_KEY"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

ALLOWED_HOSTS = []
