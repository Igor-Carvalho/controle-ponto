"""Configuração de administração da aplicação core."""

from django.contrib import admin, auth


@admin.register(auth.get_user_model())
class UserAdmin(admin.ModelAdmin):
    """Registra o usuário base na aplicação admin."""
