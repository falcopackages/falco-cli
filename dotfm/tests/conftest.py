import logging

import pytest
from django.test.utils import override_settings

pytest_plugins = []  # type: ignore


def pytest_configure(config):
    logging.disable(logging.CRITICAL)


TEST_SETTINGS = {
    "DEBUG": False,
    "CACHES": {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    },
    "EMAIL_BACKEND": "django.core.mail.backends.locmem.EmailBackend",
    "LOGGING_CONFIG": None,
    "PASSWORD_HASHERS": [
        "django.contrib.auth.hashers.MD5PasswordHasher",
    ],
    "Q_CLUSTER": {
        "sync": True,
    },
    "STORAGES": {
        "default": {
            "BACKEND": "django.core.files.storage.InMemoryStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    },
    "WHITENOISE_AUTOREFRESH": True,
}


@pytest.fixture(autouse=True, scope="session")
def use_test_settings():
    with override_settings(**TEST_SETTINGS):
        yield