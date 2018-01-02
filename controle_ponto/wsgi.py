"""wsgi module."""

import os

from django.core import wsgi

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "controle_ponto.settings")
application = wsgi.get_wsgi_application()
