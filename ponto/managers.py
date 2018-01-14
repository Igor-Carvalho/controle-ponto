"""Gerenciadores da aplicação ponto."""

import calendar
import datetime
import json

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

    def carregar_ponto(self, arquivo):
        """Carrega os dados do ponto de um usuário."""
        with arquivo as f:
            dados = json.load(f)
            dono = auth.get_user_model().objects.get(username=dados['username'])
            ponto = self.model.objects.get(dono=dono, siape=dados['siape'])
            for carga_horária_dict in dados['carga_horária']:
                carga_horária = models.CargaHorária.objects.get(
                    ano=int(carga_horária_dict['ano']),
                    ponto=ponto,
                )
                for mês_dict in carga_horária_dict['meses']:
                    mês_trabalho = models.MêsTrabalho.objects.get(
                        carga_horária=carga_horária,
                        mês=int(mês_dict['mês']),
                    )
                    for dia_dict in mês_dict['dias']:
                        dia = datetime.datetime.strptime(dia_dict.pop('dia'), '%d/%m/%Y').date()
                        models.DiaTrabalho.objects.filter(
                            mês_trabalho=mês_trabalho,
                            dia=dia.day,
                            dia_semana=dia.weekday(),
                        ).update(**dia_dict)
