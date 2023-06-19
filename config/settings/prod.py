from .base import *  # noqa


DEBUG = True
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE_PROD", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE_PROD", BASE_DIR / "db.sqlite3"),
        "USER": os.environ.get("SQL_USER_PROD", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD_PROD", "password"),
        "HOST": os.environ.get("SQL_HOST_PROD", "localhost"),
        "PORT": os.environ.get("SQL_PORT_PROD", "5432"),
    }
}

###################################################################
# Django security
###################################################################

"""
IF YOU WANT SET CSRF_TRUSTED_ORIGINS = ["*"] THEN YOU SHOULD SET:
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
"""
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

CSRF_COOKIE_SECURE = True


###################################################################
# CORS
###################################################################
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ["*"]
