"""Gerenciadores da aplicação ponto."""

import calendar

from django.contrib import auth
from django.db.models import Manager

from . import models


class PontoManager(Manager):
    """Gerenciador de ponto."""

    def iniciar_ponto(self, username, siape, ano):
        """Inicializa um ponto para um dado servidor."""
        usuário = auth.get_user_model().objects.get(username=username)
        ponto = self.model.objects.get_or_create(dono=usuário, siape=siape)[0]
        carga_horária, created = models.CargaHorária.objects.get_or_create(ponto=ponto, ano=ano)
        cal = calendar.Calendar(6)

        if created:
            for ref in range(1, 13):
                mês_trabalho = models.MêsTrabalho.objects.get_or_create(
                    carga_horária=carga_horária,
                    mês=ref
                )[0]

                for dia, dia_semana in cal.itermonthdays2(ano, ref):
                    if not dia == 0 and dia_semana not in [5, 6]:
                        models.DiaTrabalho.objects.get_or_create(
                            mês_trabalho=mês_trabalho,
                            dia=dia,
                            dia_semana=dia_semana
                        )

    def carregar_ponto(self, siape):
        """Carrega os dados do ponto de um usuário."""
