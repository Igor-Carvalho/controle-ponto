"""Inicializa o ponto para um usuário."""

import calendar
import logging
import os
import sys

from django.contrib.auth import get_user_model
from django.core.management import base

from ... import models

logger = logging.getLogger(__name__)


class Command(base.BaseCommand):
    """Comando."""

    def add_arguments(self, parser):
        """Adiciona argumentos da linha de comando."""
        parser.add_argument('ano', type=int)
        parser.add_argument('username')
        parser.add_argument('siape')

    def handle(self, **options):
        """Executa o comando."""
        if 'development' not in os.environ['DJANGO_SETTINGS_MODULE']:
            logger.info('Esse comando deve apenas ser usado em desenvolvimento.')
            sys.exit(1)

        usuário = get_user_model().objects.get(username=options['username'])
        ponto = models.Ponto.objects.get_or_create(dono=usuário, siape=options['siape'])[0]
        carga_horária, created = models.CargaHorária.objects.get_or_create(ponto=ponto, ano=options['ano'])
        cal = calendar.Calendar(6)

        if created:
            for ref in range(1, 13):
                mês_trabalho = models.MêsTrabalho.objects.get_or_create(
                    carga_horária=carga_horária,
                    mês=ref
                )[0]

                for dia, dia_semana in cal.itermonthdays2(options['ano'], ref):
                    if not dia == 0 and dia_semana not in [5, 6]:
                        models.DiaTrabalho.objects.get_or_create(
                            mês_trabalho=mês_trabalho,
                            dia=dia,
                            dia_semana=dia_semana
                        )
