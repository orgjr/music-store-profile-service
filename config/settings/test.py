from config.settings.base import *

ENV = "testing"

DEBUG = True

SECRET_KEY = "test-key"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

ALLOWED_HOSTS = ["testserver"]
