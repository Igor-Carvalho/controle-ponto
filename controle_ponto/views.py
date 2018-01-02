"""Módulo contém views genéricas ou globais ao projeto."""

from django.views import generic


class IndexView(generic.TemplateView):
    """Index."""

    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        """Contexto da página."""
        ctx = super(IndexView, self).get_context_data(**kwargs)
        ctx['mensagem_django'] = 'Django Rocks'
        return ctx


index = IndexView.as_view()
