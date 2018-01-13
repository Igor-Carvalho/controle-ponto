"""Util testes."""

import datetime
import unittest

from .. import utils


class CalculadoraTempoMixinTest(unittest.TestCase):
    """Verifica a API da CalculadoraTempoMixin."""

    def test_obter_str_tempo(self):
        """Verifica se a tupla de tempo é obtida corretamente."""
        ct = utils.CalculadoraTempoMixin()
        ct.horas_trabalhadas = datetime.datetime(1, 1, 2) - datetime.datetime(1, 1, 1)
        self.assertEqual(ct.horas_trabalhadas_str, '24:00:00')

        ct = utils.CalculadoraTempoMixin()
        ct.horas_trabalhadas = datetime.datetime(1, 1, 20) - datetime.datetime(1, 1, 1)
        self.assertEqual(ct.horas_trabalhadas_str, f'{19 * 24}:00:00')

        ct = utils.CalculadoraTempoMixin()
        ct.horas_trabalhadas = datetime.datetime(1, 1, 2, 15, 24, 12) - datetime.datetime(1, 1, 1)
        self.assertEqual(ct.horas_trabalhadas_str, '39:24:12')

        ct = utils.CalculadoraTempoMixin()
        horas_trabalhadas = datetime.datetime(1, 1, 2, 15, 24, 12) - datetime.datetime(1, 1, 1, 10, 10, 10)
        ct.horas_trabalhadas = horas_trabalhadas
        self.assertEqual(ct.horas_trabalhadas_str, '29:14:02')

        ct = utils.CalculadoraTempoMixin()
        horas_trabalhadas = datetime.datetime(1, 1, 2, 8, 24, 12) - datetime.datetime(1, 1, 1, 10, 10, 10)
        ct.horas_trabalhadas = horas_trabalhadas
        self.assertEqual(ct.horas_trabalhadas_str, '22:14:02')
