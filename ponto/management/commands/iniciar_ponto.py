"""Inicializa o ponto para um usuário."""

import logging
import os
import sys

from django.core import management

from ... import models

logger = logging.getLogger(__name__)


class Command(management.BaseCommand):
    """Comando."""

    def add_arguments(self, parser):
        """Adiciona argumentos da linha de comando."""
        parser.add_argument('username')
        parser.add_argument('siape')
        parser.add_argument('ano', type=int)

    def handle(self, **options):
        """Executa o comando."""
        if 'development' not in os.environ['DJANGO_SETTINGS_MODULE']:
            logger.info('Esse comando deve apenas ser usado em desenvolvimento.')
            sys.exit(1)

        models.Ponto.objects.iniciar_ponto(options['username'], options['siape'], options['ano'])
