"""Rotas da API."""

from rest_framework import routers

from core import views as core_views
from ponto import views as ponto_views

router = routers.DefaultRouter()
router.register('users', core_views.UserViewSet)

router.register('pontos', ponto_views.PontoViewSet)
router.register('carga-horária', ponto_views.CargaHoráriaViewSet)
router.register('meses', ponto_views.MêsTrabalhoViewSet)
router.register('dias', ponto_views.DiaTrabalhoViewSet)

urls = router.urls
