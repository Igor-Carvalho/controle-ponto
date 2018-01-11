"""Views da aplicação ponto."""

from rest_framework import generics, viewsets

from core.pagination import CorePaginator

from . import models, permissions, serializers


class PontoBaseViewSet(generics.ListCreateAPIView, generics.RetrieveUpdateAPIView, viewsets.GenericViewSet):
    """Base view set."""


class PontoViewSet(PontoBaseViewSet):
    """Viewset para pontos."""

    queryset = models.Ponto.objects.all()
    serializer_class = serializers.PontoSerializer
    permission_classes = (permissions.PontoDonoPermission,)

    def perform_create(self, serializer):
        """Adiciona o usuário atual como dono do recurso."""
        kwargs = {}
        if not self.request.user.is_superuser:
            kwargs['dono'] = self.request.user

        serializer.save(**kwargs)

    def get_queryset(self):
        """Obtém a lista de dias para o usuário dono."""
        queryset = super(PontoViewSet, self).get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(dono=self.request.user)

        return queryset


class CargaHoráriaViewSet(PontoBaseViewSet):
    """Viewset para carga horária."""

    queryset = models.CargaHorária.objects.all()
    serializer_class = serializers.CargaHoráriaSerializer
    permission_classes = (permissions.CargaHoráriaPermission,)
    filter_fields = ['ano']

    def get_queryset(self):
        """Obtém a lista de dias para o usuário dono."""
        queryset = super(CargaHoráriaViewSet, self).get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(ponto__dono=self.request.user)

        return queryset

    def get_serializer_class(self):
        """Obtém um serializador diferente para exibir mais detalhes sobre a carga horária."""
        if self.action == 'retrieve':
            return serializers.CargaHoráriaDetailSerializer

        return super(CargaHoráriaViewSet, self).get_serializer_class()


class MêsTrabalhoViewSet(PontoBaseViewSet):
    """Viewset para carga horária."""

    queryset = models.MêsTrabalho.objects.all()
    serializer_class = serializers.MêsTrabalhoSerializer
    permission_classes = (permissions.MêsTrabalhoPermission,)
    pagination_class = CorePaginator
    filter_fields = ['carga_horária__ano']

    def get_queryset(self):
        """Obtém a lista de dias para o usuário dono."""
        queryset = super(MêsTrabalhoViewSet, self).get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(carga_horária__ponto__dono=self.request.user)

        return queryset.distinct()

    def get_serializer_class(self):
        """Obtém um serializador diferente para exibir mais detalhes sobre o mês trabalho."""
        if self.action == 'retrieve':
            return serializers.MêsTrabalhoDetailSerializer

        return super(MêsTrabalhoViewSet, self).get_serializer_class()


class DiaTrabalhoViewSet(PontoBaseViewSet):
    """Viewset para dia de trabalho."""

    queryset = models.DiaTrabalho.objects.all()
    serializer_class = serializers.DiaTrabalhoSerializer
    permission_classes = (permissions.DiaTrabalhoPermission,)

    def get_queryset(self):
        """Obtém a lista de dias para o usuário dono."""
        queryset = super(DiaTrabalhoViewSet, self).get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(mês_trabalho__carga_horária__ponto__dono=self.request.user)

        return queryset
