"""Util testes."""

import datetime
import unittest

from .. import utils


class CalculadoraTempoMixinTest(unittest.TestCase):
    """Verifica a API da CalculadoraTempoMixin."""

    def test_obter_tupla_tempo(self):
        """Verifica se a tupla de tempo é obtida corretamente."""
        ct = utils.CalculadoraTempoMixin()
        ct.horas_trabalhadas = datetime.datetime(1, 1, 2) - datetime.datetime(1, 1, 1)
        self.assertTupleEqual(ct.horas_trabalhadas_tupla, (24, 0, 0))

        ct = utils.CalculadoraTempoMixin()
        ct.horas_trabalhadas = datetime.datetime(1, 1, 20) - datetime.datetime(1, 1, 1)
        self.assertTupleEqual(ct.horas_trabalhadas_tupla, (19 * 24, 0, 0))

        ct = utils.CalculadoraTempoMixin()
        ct.horas_trabalhadas = datetime.datetime(1, 1, 2, 15, 24, 12) - datetime.datetime(1, 1, 1)
        self.assertTupleEqual(ct.horas_trabalhadas_tupla, (39, 24, 12))

        horas_trabalhadas = datetime.datetime(1, 1, 2, 15, 24, 12) - datetime.datetime(1, 1, 1, 10, 10, 10)
        ct = utils.CalculadoraTempoMixin()
        ct.horas_trabalhadas = horas_trabalhadas
        self.assertTupleEqual(ct.horas_trabalhadas_tupla, (29, 14, 2))

        horas_trabalhadas = datetime.datetime(1, 1, 2, 8, 24, 12) - datetime.datetime(1, 1, 1, 10, 10, 10)
        ct = utils.CalculadoraTempoMixin()
        ct.horas_trabalhadas = horas_trabalhadas
        self.assertTupleEqual(ct.horas_trabalhadas_tupla, (22, 14, 2))
