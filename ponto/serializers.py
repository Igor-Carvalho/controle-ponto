"""Serializadores da aplicação ponto."""

import logging

from rest_framework import serializers

from . import models

logger = logging.getLogger(__name__)


class DiaTrabalhoSerializer(serializers.ModelSerializer):
    """Serializador de dias."""

    dia_semana = serializers.ReadOnlyField(source='get_dia_semana_display')

    class Meta:
        """Meta opções do serializador."""

        model = models.DiaTrabalho
        fields = ['id',
                  'mês_trabalho',
                  'dia',
                  'dia_semana',
                  'entrada_manhã',
                  'saída_manhã',
                  'entrada_tarde',
                  'saída_tarde',
                  'horas_trabalhadas',
                  'horas_trabalhadas_tupla']


class MêsTrabalhoSerializer(serializers.ModelSerializer):
    """Serializador de meses."""

    carga_horária_str = serializers.StringRelatedField(source='carga_horária')
    mês = serializers.ReadOnlyField(source='get_mês_display')

    class Meta:
        """Meta opções do serializador."""

        model = models.MêsTrabalho
        fields = ['id',
                  'mês',
                  'carga_horária',
                  'carga_horária_str',
                  'horas_trabalhadas',
                  'horas_trabalhadas_tupla']


class MêsTrabalhoDetailSerializer(MêsTrabalhoSerializer):
    """Serializador de meses."""

    dias = DiaTrabalhoSerializer(read_only=True, many=True)

    class Meta(MêsTrabalhoSerializer.Meta):
        """Meta opções do serializador."""

        fields = ['id',
                  'mês',
                  'carga_horária',
                  'carga_horária_str',
                  'horas_trabalhadas',
                  'horas_trabalhadas_tupla',
                  'dias']


class CargaHoráriaSerializer(serializers.ModelSerializer):
    """Carga horária serializer."""

    ponto_str = serializers.StringRelatedField(source='ponto')

    class Meta:
        """Meta opções do serializador."""

        model = models.CargaHorária
        fields = ['id',
                  'ponto',
                  'ponto_str',
                  'ano',
                  'horas_trabalhadas',
                  'horas_trabalhadas_tupla']


class CargaHoráriaDetailSerializer(CargaHoráriaSerializer):
    """Carga horária serializer."""

    meses = MêsTrabalhoSerializer(read_only=True, many=True)

    class Meta(CargaHoráriaSerializer.Meta):
        """Meta opções do serializador."""

        model = models.CargaHorária
        fields = ['id',
                  'ponto',
                  'ponto_str',
                  'ano',
                  'horas_trabalhadas',
                  'horas_trabalhadas_tupla',
                  'meses']


class PontoSerializer(serializers.ModelSerializer):
    """Ponto serializer."""

    dono_str = serializers.StringRelatedField(source='dono')

    class Meta:
        """Meta opções do serializador."""

        model = models.Ponto
        fields = ['id',
                  'siape',
                  'dono',
                  'dono_str']
