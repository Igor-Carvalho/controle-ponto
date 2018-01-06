"""Ponto utils."""


class CalculadoraTempoMixin:
    """Mixin para o cálculo de horas."""

    @property
    def horas_trabalhadas_tupla(self):
        """Calcula as horas trabalhadas deste dia."""
        minuto = 60
        hora = 60 * minuto

        horas = 0
        minutos = 0

        total_segundos = int(self.horas_trabalhadas.total_seconds())

        # extrai as horas do timedelta
        while total_segundos >= hora:
            total_segundos -= hora
            horas += 1

        # extrai os minutos do timedelta
        while total_segundos >= minuto:
            total_segundos -= minuto
            minutos += 1

        return (horas, minutos, total_segundos)
