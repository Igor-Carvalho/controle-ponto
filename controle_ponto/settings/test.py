"""Configurações de teste."""

from .development import *  # NOQA: F403

PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']
AUTH_PASSWORD_VALIDATORS = []
