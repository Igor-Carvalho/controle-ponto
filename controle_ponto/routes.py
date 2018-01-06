"""Rotas da API."""

from core.views import UserViewSet
from ponto.views import CargaHoráriaViewSet, DiaTrabalhoViewSet, MêsTrabalhoViewSet, PontoViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('pontos', PontoViewSet)
router.register('carga-horária', CargaHoráriaViewSet)
router.register('meses', MêsTrabalhoViewSet)
router.register('dias', DiaTrabalhoViewSet)

urls = router.urls
