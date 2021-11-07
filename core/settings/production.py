from .base import *

DEBUG = False

ALLOWED_HOSTS = ["3.67.127.172", "www.tfselcukintibak.com", "tfselcukintibak.com"]

DATABASES = {
    "default": {
        "ENGINE": os.environ.get(
            "SQL_ENGINE", "django.db.backends.postgresql_psycopg2"
        ),
        "NAME": os.environ.get("SQL_DATABASE", "intibak"),
        "USER": os.environ.get("SQL_USER", "postgres"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "Novu.2021"),
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

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")
PUBLIC_MEDIA_LOCATION = os.getenv("PUBLIC_MEDIA_LOCATION")
DEFAULT_FILE_STORAGE = os.getenv('DEFAULT_FILE_STORAGE')

# MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com//{PUBLIC_MEDIA_LOCATION}/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
