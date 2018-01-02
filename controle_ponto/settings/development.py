"""Configurações de desenvolvimento."""

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# Django Debug Toolbar
INSTALLED_APPS += ['debug_toolbar']
INTERNAL_IPS = ['127.0.0.1']

MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE  # NOQA: F405

MEDIA_ROOT = root.path('')('media_test')
