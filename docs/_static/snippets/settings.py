import multiprocessing
import os
import sys
from email.utils import parseaddr
from pathlib import Path

import sentry_sdk
from environs import Env
from falco_toolbox.sentry import sentry_profiles_sampler, sentry_traces_sampler
from marshmallow.validate import Email, OneOf
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

# 0. Setup
# --------------------------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

APPS_DIR = BASE_DIR / "myjourney"

env = Env()
env.read_env(Path(BASE_DIR, ".env").as_posix())

# We should strive to only have two possible runtime scenarios: either `DEBUG`
# is True or it is False. `DEBUG` should be only true in development, and
# False when deployed, whether or not it's a production environment.
DEBUG = env.bool("DEBUG", default=False)

# 1. Django Core Settings
# -----------------------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.0/ref/settings/

ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS", default=["*"] if DEBUG else ["localhost"], subcast=str
)

ASGI_APPLICATION = "myjourney.asgi.application"

# https://grantjenks.com/docs/diskcache/tutorial.html#djangocache
if "CACHE_LOCATION" in os.environ:
    CACHES = {
        "default": {
            "BACKEND": "diskcache.DjangoCache",
            "LOCATION": env.str("CACHE_LOCATION"),
            "TIMEOUT": 300,
            "SHARDS": 8,
            "DATABASE_TIMEOUT": 0.010,  # 10 milliseconds
            "OPTIONS": {"size_limit": 2**30},  # 1 gigabyte
        }
    }

CSRF_COOKIE_SECURE = not DEBUG

DATABASES = {
    "default": env.dj_db_url("DATABASE_URL", default="sqlite:///db.sqlite3"),
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

if not DEBUG:
    DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)
    DATABASES["default"]["CONN_HEALTH_CHECKS"] = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DEFAULT_FROM_EMAIL = env.str(
    "DEFAULT_FROM_EMAIL",
    default="tobidegnon@proton.me",
    validate=lambda v: Email()(parseaddr(v)[1]),
)

EMAIL_BACKEND = (
    "django.core.mail.backends.console.EmailBackend"
    if DEBUG
    else "anymail.backends.amazon_ses.EmailBackend"
)

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.forms",
]

THIRD_PARTY_APPS = [
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "compressor",
    "crispy_forms",
    "crispy_tailwind",
    "django_extensions",
    "django_htmx",
    "django_q",
    "django_q_registry",
    "django_tailwind_cli",
    "falco_ui.favicons",
    "falco_toolbox",
    "health_check",
    "health_check.cache",
    "health_check.contrib.migrations",
    "health_check.db",
    "health_check.storage",
    "heroicons",
    "template_partials",
    "unique_user_email",
]

LOCAL_APPS = [
    "myjourney.core",
    "myjourney.entries",
]

if DEBUG:
    # Development only apps
    THIRD_PARTY_APPS = [
        "debug_toolbar",
        "whitenoise.runserver_nostatic",
        "django_browser_reload",
        "django_fastdev",
        "django_watchfiles",
        *THIRD_PARTY_APPS,
    ]

INSTALLED_APPS = LOCAL_APPS + THIRD_PARTY_APPS + DJANGO_APPS

if DEBUG:
    INTERNAL_IPS = [
        "127.0.0.1",
        "10.0.2.2",
    ]

LANGUAGE_CODE = "en-us"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "plain_console": {
            "format": "%(levelname)s %(message)s",
        },
        "verbose": {
            "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        },
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["stdout"],
            "level": env.log_level("DJANGO_LOG_LEVEL", default="INFO"),
        },
        "myjourney": {
            "handlers": ["stdout"],
            "level": env.log_level("MYJOURNEY_LOG_LEVEL", default="INFO"),
        },
    },
}

MEDIA_ROOT = env.path("MEDIA_ROOT", default=APPS_DIR / "media")

MEDIA_URL = "/media/"

# https://docs.djangoproject.com/en/dev/topics/http/middleware/
# https://docs.djangoproject.com/en/dev/ref/middleware/#middleware-ordering
MIDDLEWARE = [
    # should be first
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # order doesn't matter
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    # should be last
    "django.middleware.cache.FetchFromCacheMiddleware",
]
if DEBUG:
    MIDDLEWARE.remove("django.middleware.cache.UpdateCacheMiddleware")
    MIDDLEWARE.remove("django.middleware.cache.FetchFromCacheMiddleware")
    MIDDLEWARE.append("django_browser_reload.middleware.BrowserReloadMiddleware")

    MIDDLEWARE.insert(
        MIDDLEWARE.index("django.middleware.common.CommonMiddleware") + 1,
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    )

ROOT_URLCONF = "myjourney.urls"

SECRET_KEY = env.str(
    "SECRET_KEY", default="django-insecure-d_dRMqfvTiJEYXCHtWr3SHukogK6H-kIRZehUo3n1Lc"
)

SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG

SECURE_HSTS_PRELOAD = not DEBUG

# https://docs.djangoproject.com/en/dev/ref/middleware/#http-strict-transport-security
# 2 minutes to start with, will increase as HSTS is tested
# example of production value: 60 * 60 * 24 * 7 = 604800 (1 week)
SECURE_HSTS_SECONDS = 0 if DEBUG else env.int("SECURE_HSTS_SECONDS", default=60 * 2)

# https://noumenal.es/notes/til/django/csrf-trusted-origins/
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_SSL_REDIRECT = not DEBUG

SERVER_EMAIL = env.str(
    "SERVER_EMAIL",
    default=DEFAULT_FROM_EMAIL,
    validate=lambda v: Email()(parseaddr(v)[1]),
)

SESSION_COOKIE_SECURE = not DEBUG

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": env.str("AWS_ACCESS_KEY_ID", default=None),
            "bucket_name": env.str("AWS_STORAGE_BUCKET_NAME", default=None),
            "region_name": env.str("AWS_S3_REGION_NAME", default=None),
            "secret_key": env.str("AWS_SECRET_ACCESS_KEY", default=None),
        },
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
if DEBUG and not env.bool("USE_S3", default=False):
    STORAGES["default"] = {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    }

# https://nickjanetakis.com/blog/django-4-1-html-templates-are-cached-by-default-with-debug-true
DEFAULT_LOADERS = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]

CACHED_LOADERS = [("django.template.loaders.cached.Loader", DEFAULT_LOADERS)]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(APPS_DIR / "templates")],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "builtins": [
                "template_partials.templatetags.partials",
                "heroicons.templatetags.heroicons",
            ],
            "debug": DEBUG,
            "loaders": [
                (
                    "template_partials.loader.Loader",
                    DEFAULT_LOADERS if DEBUG else CACHED_LOADERS,
                )
            ],
        },
    },
]

TIME_ZONE = "UTC"

USE_I18N = False

USE_TZ = True

WSGI_APPLICATION = "myjourney.wsgi.application"

# 2. Django Contrib Settings
# -----------------------------------------------------------------------------------------------

# django.contrib.auth
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
if DEBUG:
    AUTH_PASSWORD_VALIDATORS = []

# django.contrib.staticfiles
STATIC_ROOT = APPS_DIR / "staticfiles"

STATIC_URL = "/static/"

STATICFILES_DIRS = [APPS_DIR / "static"]

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

# 3. Third Party Settings
# -------------------------------------------------------------------------------------------------

# django-allauth
ACCOUNT_AUTHENTICATION_METHOD = "email"

ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http" if DEBUG else "https"

ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_LOGOUT_REDIRECT_URL = "account_login"

ACCOUNT_SESSION_REMEMBER = True

ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False

ACCOUNT_UNIQUE_EMAIL = True

ACCOUNT_USERNAME_REQUIRED = False

LOGIN_REDIRECT_URL = "home"

# django-anymail
if not DEBUG:
    ANYMAIL = {
        "AMAZON_SES_CLIENT_PARAMS": {
            "aws_access_key_id": env.str("AWS_ACCESS_KEY_ID", default=None),
            "aws_secret_access_key": env.str("AWS_SECRET_ACCESS_KEY", default=None),
            "region_name": env.str("AWS_S3_REGION_NAME", default=None),
        }
    }

# django-compressor
COMPRESS_OFFLINE = not DEBUG
COMPRESS_FILTERS = {
    "css": [
        "compressor.filters.css_default.CssAbsoluteFilter",
        "compressor.filters.cssmin.rCSSMinFilter",
        "refreshcss.filters.RefreshCSSFilter",
    ],
    "js": ["compressor.filters.jsmin.rJSMinFilter"],
}

# django-crispy-forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"

CRISPY_TEMPLATE_PACK = "tailwind"

# django-debug-toolbar
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
    "SHOW_COLLAPSED": True,
    "UPDATE_ON_FETCH": True,
    "ROOT_TAG_EXTRA_ATTRS": "hx-preserve",
}

# django-q2
Q_CLUSTER = {
    "name": "ORM",
    "workers": multiprocessing.cpu_count() * 2 + 1,
    "timeout": 60 * 10,  # 10 minutes
    "retry": 60 * 12,  # 12 minutes
    "queue_limit": 50,
    "bulk": 10,
    "orm": "default",
}

# sentry
if (SENTRY_DSN := env.url("SENTRY_DSN", default=None)).scheme and not DEBUG:
    sentry_sdk.init(
        dsn=SENTRY_DSN.geturl(),
        environment=env.str(
            "SENTRY_ENV",
            default="development",
            validate=OneOf(["development", "production"]),
        ),
        integrations=[
            DjangoIntegration(),
            LoggingIntegration(event_level=None, level=None),
        ],
        traces_sampler=sentry_traces_sampler,
        profiles_sampler=sentry_profiles_sampler,
        send_default_pii=True,
    )

# 4. Project Settings
# -----------------------------------------------------------------------------------------------------

ADMIN_URL = env.str("ADMIN_URL", default="admin/")
