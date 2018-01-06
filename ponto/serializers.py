"""Serializadores da aplicação ponto."""

import logging

from rest_framework import serializers

from . import models

logger = logging.getLogger(__name__)


class DiaTrabalhoSerializer(serializers.ModelSerializer):
    """Serializador de dias."""

    mês_trabalho_str = serializers.StringRelatedField(source='mês_trabalho')

    class Meta:
        """Meta opções do serializador."""

        model = models.DiaTrabalho
        fields = 'id mês_trabalho dia entrada_manhã saída_manhã entrada_tarde saída_tarde horas_trabalhadas '
        fields += 'horas_trabalhadas_tupla mês_trabalho_str'
        fields = fields.split()


class MêsTrabalhoSerializer(serializers.ModelSerializer):
    """Serializador de meses."""

    carga_horária_str = serializers.StringRelatedField(source='carga_horária')

    class Meta:
        """Meta opções do serializador."""

        model = models.MêsTrabalho
        fields = 'id carga_horária referência horas_trabalhadas horas_trabalhadas_tupla carga_horária_str'
        fields = fields.split()


class CargaHoráriaSerializer(serializers.ModelSerializer):
    """Carga horária serializer."""

    ponto_str = serializers.StringRelatedField(source='ponto')

    class Meta:
        """Meta opções do serializador."""

        model = models.CargaHorária
        fields = 'id ponto ano ponto_str horas_trabalhadas horas_trabalhadas_tupla'.split()


class PontoSerializer(serializers.ModelSerializer):
    """Ponto serializer."""

    dono_str = serializers.StringRelatedField(source='dono')

    class Meta:
        """Meta opções do serializador."""

        model = models.Ponto
        fields = 'id siape dono dono_str'.split()
