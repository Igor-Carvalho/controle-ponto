"""Inicializa o ponto para um usuário."""

import logging

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
        logger.info(f'Criação de planilha de dados para o usuário {options["username"]} iniciada...')
        models.Ponto.objects.iniciar_ponto(options['username'], options['siape'], options['ano'])
        logger.info('Planilha criada com sucesso.')
