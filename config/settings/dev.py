from .base import *  # noqa


DEBUG = True

STAGE = "develop"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
CSRF_TRUSTED_ORIGINS = ["https://khodjiyev2o.jprq.live", "https://web.mintapp.info"]
