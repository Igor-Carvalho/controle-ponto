"""Rotas da API."""

from core.views import UserViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', UserViewSet)

urls = router.urls
