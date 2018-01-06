"""Util testes."""

import datetime
import unittest

from .. import utils


class CalculadoraTempoMixinTest(unittest.TestCase):
    """Verifica a API da CalculadoraTempoMixin."""

    def test_obter_tupla_tempo(self):
        """Verifica se a tupla de tempo é obtida corretamente."""
        d1, d2 = datetime.datetime(2017, 1, 1), datetime.datetime(2017, 1, 2)
        ct = utils.CalculadoraTempoMixin().obter_tupla_tempo(d1, d2)
        self.assertTupleEqual(ct, (24, 0, 0))

        d1, d2 = datetime.datetime(2017, 1, 1), datetime.datetime(2017, 1, 20)
        ct = utils.CalculadoraTempoMixin().obter_tupla_tempo(d1, d2)
        self.assertTupleEqual(ct, (19 * 24, 0, 0))

        d1, d2 = datetime.datetime(2017, 1, 1), datetime.datetime(2017, 1, 2, 15, 24, 12)
        ct = utils.CalculadoraTempoMixin().obter_tupla_tempo(d1, d2)
        self.assertTupleEqual(ct, (39, 24, 12))

        d1, d2 = datetime.datetime(2017, 1, 1, 10, 10, 10), datetime.datetime(2017, 1, 2, 15, 24, 12)
        ct = utils.CalculadoraTempoMixin().obter_tupla_tempo(d1, d2)
        self.assertTupleEqual(ct, (29, 14, 2))

        d1, d2 = datetime.datetime(2017, 1, 1, 10, 10, 10), datetime.datetime(2017, 1, 2, 8, 24, 12)
        ct = utils.CalculadoraTempoMixin().obter_tupla_tempo(d1, d2)
        self.assertTupleEqual(ct, (22, 14, 2))
