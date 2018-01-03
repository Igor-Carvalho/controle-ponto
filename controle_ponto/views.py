"""Módulo contém views genéricas ou globais ao projeto."""

from django.contrib.auth import mixins
from django.views import generic


class DashboardView(mixins.LoginRequiredMixin, generic.TemplateView):
    """Index."""

    template_name = 'dashboard.html'


dashboard = DashboardView.as_view()
