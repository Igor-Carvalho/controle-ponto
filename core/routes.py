"""Rotas da api da aplicação core."""

from . import views


def registrar_api(router):
    """Registra as rotas da aplicação."""
    router.register('users', views.UserViewSet)
