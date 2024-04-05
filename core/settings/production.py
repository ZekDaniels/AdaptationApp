from .base import *

DEBUG = False

ALLOWED_HOSTS = ["www.tfselcukintibak.com", "tfselcukintibak.com"]

DATABASES = {
    "default": {
        "ENGINE": os.environ.get(
            "SQL_ENGINE", "django.db.backends.postgresql_psycopg2"
        ),
        "NAME": os.environ.get("SQL_DATABASE", "intibak"),
        "USER": os.environ.get("SQL_USER", "postgres"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "ni-chrome.nothinghosting.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 25
EMAIL_HOST_USER = "info@nothing.com"
EMAIL_HOST_PASSWORD = "nothing"
DEFAULT_FROM_EMAIL = "Nothing <nothing@nothing.com>"

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# SECURE_SSL_REDIRECT = True

# https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-SESSION_COOKIE_SECURE
# SESSION_COOKIE_SECURE = True

# https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-CSRF_COOKIE_SECURE
# CSRF_COOKIE_SECURE = True

SECURE_BROWSER_XSS_FILTER = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
STATICFILES_DIRS = (
    os.path.join('static/fonts'),
    os.path.join('static/images'),
)
