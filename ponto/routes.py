"""Rotas da api da aplicação ponto."""

from . import views


def registrar_api(router):
    """Registra as rotas da aplicação."""
    router.register('pontos', views.PontoViewSet)
    router.register('carga-horária', views.CargaHoráriaViewSet)
    router.register('meses', views.MêsTrabalhoViewSet)
    router.register('dias', views.DiaTrabalhoViewSet)
