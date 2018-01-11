"""Modelos da aplicação ponto."""

import datetime
import logging

from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel

from . import utils

logger = logging.getLogger(__name__)


class Ponto(TimeStampedModel):
    """Histórico completo da jornada de trabalho do servidor ao logo dos anos."""

    dono = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='pontos')
    siape = models.CharField(max_length=16)
    histórico = AuditlogHistoryField()

    class Meta:
        """Meta opções do modelo."""

        ordering = ['id']

    def __str__(self):
        """toString."""
        return f'Ponto de trabalho referente ao servidor siape nº {self.siape} ({self.dono})'

    __repr__ = __str__


auditlog.register(Ponto)


class CargaHorária(utils.CalculadoraTempoMixin, TimeStampedModel):
    """Carga horária contendo os meses de trabalho anuais."""

    ponto = models.ForeignKey(Ponto, related_name='carga_horária')
    ano = models.IntegerField()
    histórico = AuditlogHistoryField()

    class Meta:
        """Meta opções do modelo."""

        ordering = ['ano']

    @property
    def horas_trabalhadas(self):
        """Horas trabalhadas totais dessa carga horária."""
        total = datetime.timedelta()
        for mês in self.meses.all():
            total += mês.horas_trabalhadas

        return total

    def __str__(self):
        """toString."""
        return f'Carga horária referente ao ano {self.ano} do servidor siape nº {self.ponto.siape}'

    __repr__ = __str__


auditlog.register(CargaHorária)


class MêsTrabalho(utils.CalculadoraTempoMixin, TimeStampedModel):
    """Um mês de trabalho referente a uma carga horária mensal."""

    meses_trabalho = [(1, 'Janeiro'),
                      (2, 'Fevereiro'),
                      (3, 'Março'),
                      (4, 'Abril'),
                      (5, 'Maio'),
                      (6, 'Junho'),
                      (7, 'Julho'),
                      (8, 'Agosto'),
                      (9, 'Setembro'),
                      (10, 'Outubro'),
                      (11, 'Novembro'),
                      (12, 'Dezembro')]

    carga_horária = models.ForeignKey(CargaHorária, related_name='meses')
    mês = models.IntegerField(choices=meses_trabalho)
    histórico = AuditlogHistoryField()

    class Meta:
        """Meta opções do modelo."""

        ordering = ['mês']

    @property
    def horas_trabalhadas(self):
        """Horas trabalhadas no mês."""
        total = datetime.timedelta()
        for dia in self.dias.all():
            total += dia.horas_trabalhadas

        return total

    def __str__(self):
        """toString."""
        msg = f'Mês de trabalho referente a {self.get_mês_display()} de {self.carga_horária.ano} '
        msg += f'do servidor siape nº {self.carga_horária.ponto.siape} ({self.carga_horária.ponto.dono})'
        return msg

    __repr__ = __str__


auditlog.register(MêsTrabalho)


class DiaTrabalho(utils.CalculadoraTempoMixin, TimeStampedModel):
    """Um mês de trabalho referente a uma carga horária mensal."""

    dias_semana = [
        (6, 'Domingo'),
        (5, 'Sábado'),
        (4, 'Sexta-feira'),
        (3, 'Quinta-feira'),
        (2, 'Quarta-feira'),
        (1, 'Terça-feira'),
        (0, 'Segunda-feira'),
    ]

    mês_trabalho = models.ForeignKey(MêsTrabalho, related_name='dias')

    dia = models.IntegerField()
    dia_semana = models.IntegerField(choices=dias_semana)
    entrada_manhã = models.TimeField(default=datetime.time.min)
    saída_manhã = models.TimeField(default=datetime.time.min)
    entrada_tarde = models.TimeField(default=datetime.time.min)
    saída_tarde = models.TimeField(default=datetime.time.min)
    observação = models.TextField()

    histórico = AuditlogHistoryField()

    class Meta:
        """Meta opções do modelo."""

        ordering = ['dia']

    @property
    def horas_trabalhadas(self):
        """TODO."""
        entrada_manhã = datetime.datetime.combine(datetime.date.min, self.entrada_manhã)
        saída_manhã = datetime.datetime.combine(datetime.date.min, self.saída_manhã)

        entrada_tarde = datetime.datetime.combine(datetime.date.min, self.entrada_tarde)
        saída_tarde = datetime.datetime.combine(datetime.date.min, self.saída_tarde)

        # normalmente esses erros de conversão acontecem devido a dados enviados pelo cliente. Por enquanto,
        # são ignorados.
        try:
            return saída_tarde - entrada_tarde + saída_manhã - entrada_manhã

        except Exception as e:
            return '00:00:00'

    def __str__(self):
        """toString."""
        return f'Dia de trabalho ({self.dia})'

    __repr__ = __str__


auditlog.register(DiaTrabalho)
