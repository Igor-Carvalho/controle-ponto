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

    class Meta:
        """Meta opções do modelo."""

        ordering = ['id']

    dono = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='pontos')

    siape = models.CharField(max_length=16)

    histórico = AuditlogHistoryField()

    def __str__(self):
        """toString."""
        return f'Ponto de trabalho referente ao servidor siape nº {self.siape}'

    __repr__ = __str__


auditlog.register(Ponto)


class CargaHorária(utils.CalculadoraTempoMixin, TimeStampedModel):
    """Carga horária contendo os meses de trabalho anuais."""

    class Meta:
        """Meta opções do modelo."""

        ordering = ['ano']

    ponto = models.ForeignKey(Ponto, related_name='carga_horária')

    ano = models.IntegerField()

    histórico = AuditlogHistoryField()

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

    class Meta:
        """Meta opções do modelo."""

        ordering = ['mês']

    meses_trabalho = [('01', 'Janeiro'),
                      ('02', 'Fevereiro'),
                      ('03', 'Março'),
                      ('04', 'Abril'),
                      ('05', 'Maio'),
                      ('06', 'Junho'),
                      ('07', 'Julho'),
                      ('08', 'Agosto'),
                      ('09', 'Setembro'),
                      ('10', 'Outubro'),
                      ('11', 'Novembro'),
                      ('12', 'Dezembro')]

    carga_horária = models.ForeignKey(CargaHorária, related_name='meses')

    mês = models.CharField(max_length=2, choices=meses_trabalho, default='01')

    histórico = AuditlogHistoryField()

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

    class Meta:
        """Meta opções do modelo."""

        ordering = ['dia']

    mês_trabalho = models.ForeignKey(MêsTrabalho, related_name='dias')

    dias_semana = [
        (6, 'Domingo'),
        (5, 'Sábado'),
        (4, 'Sexta-feira'),
        (3, 'Quinta-feira'),
        (2, 'Quarta-feira'),
        (1, 'Terça-feira'),
        (0, 'Segunda-feira'),
    ]

    dia = models.IntegerField()
    dia_semana = models.IntegerField(choices=dias_semana)
    entrada_manhã = models.TimeField(default=datetime.time.min)
    saída_manhã = models.TimeField(default=datetime.time.min)
    entrada_tarde = models.TimeField(default=datetime.time.min)
    saída_tarde = models.TimeField(default=datetime.time.min)
    observação = models.TextField()

    histórico = AuditlogHistoryField()

    @property
    def horas_trabalhadas(self):
        """TODO."""
        entrada_manhã = datetime.datetime.combine(datetime.date.min, self.entrada_manhã)
        saída_manhã = datetime.datetime.combine(datetime.date.min, self.saída_manhã)

        entrada_tarde = datetime.datetime.combine(datetime.date.min, self.entrada_tarde)
        saída_tarde = datetime.datetime.combine(datetime.date.min, self.saída_tarde)
        return saída_tarde - entrada_tarde + saída_manhã - entrada_manhã

    def __str__(self):
        """toString."""
        return f'Dia de trabalho ({self.dia})'

    __repr__ = __str__


auditlog.register(DiaTrabalho)
