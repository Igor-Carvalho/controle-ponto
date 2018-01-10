"""Configurações de teste."""

from .development import *  # noqa

PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']
AUTH_PASSWORD_VALIDATORS = []
