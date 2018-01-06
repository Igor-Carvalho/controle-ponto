"""Views da aplicação ponto."""

import calendar
import datetime

from rest_framework import decorators, generics, viewsets, response

from . import models, permissions, serializers


class PontoBaseViewSet(generics.ListCreateAPIView, generics.RetrieveUpdateAPIView, viewsets.GenericViewSet):
    """Base view set."""


class PontoViewSet(PontoBaseViewSet):
    """Viewset para pontos."""

    queryset = models.Ponto.objects.all()
    serializer_class = serializers.PontoSerializer
    permission_classes = (permissions.PontoDonoPermission,)

    @decorators.list_route(methods=['post'], url_path='inicializar-ponto')
    def inicializar_ponto(self, pk=None):
        """Cria um ponto referente ao ano que o usuário acessa a app."""
        cal = calendar.Calendar(6)
        ano = self.request.query_params.get('ano', None) or datetime.date.today().year
        ano = int(ano)

        ponto = models.Ponto.objects.get_or_create(dono=self.request.user)[0]
        carga_horária, created = models.CargaHorária.objects.get_or_create(ponto=ponto, ano=ano)

        if created:
            for ref in range(1, 13):
                mês_trabalho = models.MêsTrabalho.objects.get_or_create(carga_horária=carga_horária,
                                                                        mês='{:02d}'.format(ref))[0]

                for dia, dia_semana in cal.itermonthdays2(ano, ref):
                    if not dia == 0 and dia_semana not in [5, 6]:
                        models.DiaTrabalho.objects.get_or_create(mês_trabalho=mês_trabalho,
                                                                 dia=dia, dia_semana=dia_semana)

        return response.Response({'detail': 'Ponto inicializado com sucesso.'})

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

    def get_queryset(self):
        """Obtém a lista de dias para o usuário dono."""
        queryset = super(MêsTrabalhoViewSet, self).get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(carga_horária__ponto__dono=self.request.user)

        return queryset

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
