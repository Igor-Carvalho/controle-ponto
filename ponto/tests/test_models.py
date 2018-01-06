"""Model testes."""

import datetime

from django import test
from django.contrib.auth import get_user_model

from .. import models


class ModelsTest(test.TestCase):
    """TODO."""

    @classmethod
    def setUpTestData(cls):
        """Class fixtures."""
        super(ModelsTest, cls).setUpTestData()
        cls.user = get_user_model().objects.create_user('user', 'user@domain.com', 'pass')
        cls.ponto = models.Ponto.objects.create(dono=cls.user, siape='1706059')
        cls.carga_horária = models.CargaHorária.objects.create(ponto=cls.ponto, ano=2018)
        cls.mês_trabalho = models.MêsTrabalho.objects.create(carga_horária=cls.carga_horária, referência='01')

    def test_horas_trabalhadas(self):
        """TODO."""
        dia1 = models.DiaTrabalho.objects.create(
            mês=self.mês_trabalho,
            dia=1,
            entrada_manhã=datetime.datetime(1, 1, 1, 7, 35, 0).time(),
            saída_manhã=datetime.datetime(1, 1, 1, 11, 30, 0).time(),
            entrada_tarde=datetime.datetime(1, 1, 1, 12, 30, 0).time(),
            saída_tarde=datetime.datetime(1, 1, 1, 17, 49, 0).time(),
        )
        self.assertEqual(dia1.horas_trabalhadas_tupla, (9, 14, 0))

        dia2 = models.DiaTrabalho.objects.create(
            mês=self.mês_trabalho,
            dia=2,
            entrada_manhã=datetime.datetime(1, 1, 1, 7, 25, 0).time(),
            saída_manhã=datetime.datetime(1, 1, 1, 11, 45, 0).time(),
            entrada_tarde=datetime.datetime(1, 1, 1, 12, 45, 0).time(),
            saída_tarde=datetime.datetime(1, 1, 1, 16, 49, 0).time(),
        )
        self.assertEqual(dia2.horas_trabalhadas_tupla, (8, 24, 0))

        dia3 = models.DiaTrabalho.objects.create(
            mês=self.mês_trabalho,
            dia=2,
            entrada_manhã=datetime.datetime(1, 1, 1, 7, 25, 0).time(),
            saída_manhã=datetime.datetime(1, 1, 1, 11, 45, 0).time(),
            entrada_tarde=datetime.datetime(1, 1, 1, 12, 45, 0).time(),
            saída_tarde=datetime.datetime(1, 1, 1, 16, 49, 0).time(),
        )
        self.assertEqual(dia3.horas_trabalhadas_tupla, (8, 24, 0))

        self.assertEqual(self.mês_trabalho.horas_trabalhadas_tupla, (26, 2, 0))
