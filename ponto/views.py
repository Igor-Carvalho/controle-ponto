"""Views da aplicação ponto."""

from rest_framework import generics, viewsets, permissions

from . import models, serializers


class PontoBaseViewSet(generics.ListCreateAPIView, generics.RetrieveUpdateAPIView, viewsets.GenericViewSet):
    """Base view set."""

    permission_classes = (permissions.IsAuthenticated,)


class PontoViewSet(PontoBaseViewSet):
    """Viewset para pontos."""

    queryset = models.Ponto.objects.all()
    serializer_class = serializers.PontoSerializer

    def perform_create(self, serializer):
        """Adiciona o usuário atual como dono do recurso."""
        kwargs = {}
        if not self.request.user.is_superuser:
            kwargs['dono'] = self.request.user

        serializer.save(**kwargs)


class CargaHoráriaViewSet(PontoBaseViewSet):
    """Viewset para carga horária."""

    queryset = models.CargaHorária.objects.all()
    serializer_class = serializers.CargaHoráriaSerializer


class MêsTrabalhoViewSet(PontoBaseViewSet):
    """Viewset para carga horária."""

    queryset = models.MêsTrabalho.objects.all()
    serializer_class = serializers.MêsTrabalhoSerializer


class DiaTrabalhoViewSet(PontoBaseViewSet):
    """Viewset para dia de trabalho."""

    queryset = models.DiaTrabalho.objects.all()
    serializer_class = serializers.DiaTrabalhoSerializer
