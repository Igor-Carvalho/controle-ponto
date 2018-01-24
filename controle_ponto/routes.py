"""Rotas da API."""

from rest_framework import routers

from core import routes as core_routes
from ponto import routes as ponto_routes

router = routers.DefaultRouter()
core_routes.registrar_api(router)
ponto_routes.registrar_api(router)

urls = router.urls
