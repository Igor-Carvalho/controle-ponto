"""Permissões da aplicação ponto."""

from rest_framework import permissions


class PontoDonoPermission(permissions.IsAuthenticated):
    """Permissão de acesso apenas ao dono do recurso."""

    def has_object_permission(self, request, view, obj):
        """TODO."""
        return request.user.is_superuser or request.user == obj.dono


class CargaHoráriaPermission(permissions.IsAuthenticated):
    """Permissão de acesso apenas ao dono do recurso."""

    def has_object_permission(self, request, view, obj):
        """TODO."""
        return request.user.is_superuser or request.user == obj.ponto.dono


class MêsTrabalhoPermission(permissions.IsAuthenticated):
    """Permissão de acesso apenas ao dono do recurso."""

    def has_object_permission(self, request, view, obj):
        """TODO."""
        return request.user.is_superuser or request.user == obj.carga_horária.ponto.dono


class DiaTrabalhoPermission(permissions.IsAuthenticated):
    """Permissão de acesso apenas ao dono do recurso."""

    def has_object_permission(self, request, view, obj):
        """TODO."""
        return request.user.is_superuser or request.user == obj.mês_trabalho.carga_horária.ponto.dono
