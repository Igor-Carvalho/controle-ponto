"""Módulo contém views genéricas ou globais ao projeto."""

import django_weasyprint
from django.contrib.auth import mixins
from django.contrib.staticfiles import storage
from django.views import generic

from ponto.models import DiaTrabalho

static_storage = storage.StaticFilesStorage()


class DashboardView(mixins.LoginRequiredMixin, generic.TemplateView):
    """Index."""

    template_name = 'dashboard.html'


dashboard = DashboardView.as_view()


class Relatório(django_weasyprint.WeasyTemplateView):
    """Relatório teste."""

    template_name = 'core/relatórios/a4.html'
    pdf_stylesheets = [
        static_storage.path('bootstrap/dist/css/bootstrap.min.css'),
        static_storage.path('css/relatórios/base.css'),
    ]

    def get_context_data(self, **kwargs):
        """Contexto."""
        ctx = super(Relatório, self).get_context_data(**kwargs)
        ctx['dias'] = DiaTrabalho.objects.all()[:22]
        ctx['total'] = ctx['dias'].count()
        return ctx


relatório = Relatório.as_view()
