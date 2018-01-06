"""Ponto utils."""

import datetime


class CalculadoraTempoMixin:
    """Mixin para o cálculo de horas."""

    def obter_tupla_tempo(self, d1, d2):
        """TODO."""
        minuto = 60
        hora = 60 * minuto

        horas = 0
        minutos = 0

        total_segundos = int((d2 - d1).total_seconds())

        # extrai as horas do timedelta
        while total_segundos >= hora:
            total_segundos -= hora
            horas += 1

        # extrai os minutos do timedelta
        while total_segundos >= minuto:
            total_segundos -= minuto
            minutos += 1

        return (horas, minutos, total_segundos)

    @property
    def horas_trabalhadas_tupla(self):
        """Calcula as horas trabalhadas deste dia."""
        return self.obter_tupla_tempo(
            datetime.datetime.min,
            datetime.datetime.min + self.horas_trabalhadas
        )
