"""Módulo de configuração celery."""

import os

import celery
from django.conf import settings

app = celery.Celery('controle_ponto')
app.config_from_object(os.environ['DJANGO_SETTINGS_MODULE'])
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
