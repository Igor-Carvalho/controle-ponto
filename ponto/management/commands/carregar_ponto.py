"""Comando para carregar dados de carga horária utilizando um arquivo."""

from django.core import management

from ... import models


class Command(management.BaseCommand):
    """Comando."""

    def add_arguments(self, parser):
        """Configura opções da linha de comando."""
        parser.add_argument('arquivo', type=open)

    def handle(self, **options):
        """Executa o comando."""
        models.Ponto.objects.carregar_ponto(options['arquivo'])
