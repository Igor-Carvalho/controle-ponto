"""Serializadores da aplicação ponto."""

import logging

from rest_framework import serializers

from . import models

logger = logging.getLogger(__name__)


class DiaTrabalhoSerializer(serializers.ModelSerializer):
    """Serializador de dias."""

    class Meta:
        """Meta opções do serializador."""

        model = models.DiaTrabalho
        fields = 'id mês dia entrada_manhã saída_manhã entrada_tarde saída_tarde horas_trabalhadas '
        fields += 'horas_trabalhadas_tupla'
        fields = fields.split()

    def to_representation(self, dia_trabalho):
        """toString."""
        data = super(DiaTrabalhoSerializer, self).to_representation(dia_trabalho)
        data['mês_str'] = str(dia_trabalho.mês)
        return data


class MêsTrabalhoSerializer(serializers.ModelSerializer):
    """Serializador de meses."""

    class Meta:
        """Meta opções do serializador."""

        model = models.MêsTrabalho
        fields = 'id carga_horária referência horas_trabalhadas horas_trabalhadas_tupla'.split()

    def to_representation(self, mês_trabalho):
        """toString."""
        data = super(MêsTrabalhoSerializer, self).to_representation(mês_trabalho)
        return data


class CargaHoráriaSerializer(serializers.ModelSerializer):
    """Carga horária serializer."""

    class Meta:
        """Meta opções do serializador."""

        model = models.CargaHorária
        fields = 'id ponto ano'.split()

    def to_representation(self, carga_horária):
        """toString."""
        data = super(CargaHoráriaSerializer, self).to_representation(carga_horária)
        data['ponto_str'] = str(carga_horária.ponto)
        return data


class PontoSerializer(serializers.ModelSerializer):
    """Ponto serializer."""

    class Meta:
        """Meta opções do serializador."""

        model = models.Ponto
        fields = 'id siape dono'.split()

    def to_representation(self, ponto):
        """toString."""
        data = super(PontoSerializer, self).to_representation(ponto)
        data['dono_str'] = str(ponto.dono)
        return data
