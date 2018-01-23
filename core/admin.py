"""Configuração de administração da aplicação core."""

from django.contrib import admin, auth
from django.contrib.auth.admin import UserAdmin
from hijack_admin.admin import HijackUserAdminMixin


@admin.register(auth.get_user_model())
class UsuárioAdmin(HijackUserAdminMixin, UserAdmin):
    """Registra o usuário base na aplicação admin."""

    def get_list_display(self, request):
        """Adiciona o botão para impersonar um dado usuário."""
        return super(UsuárioAdmin, self).get_list_display(request) + ('hijack_field',)
