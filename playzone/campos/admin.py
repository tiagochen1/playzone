from __future__ import annotations

from django.contrib import admin

from .models import Campo, Desporto, Reserva


@admin.register(Desporto)
class DesportoAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)


@admin.register(Campo)
class CampoAdmin(admin.ModelAdmin):
    list_display = ("nome", "estado", "preco_hora")
    list_filter = ("estado", "desportos")
    search_fields = ("nome",)
    filter_horizontal = ("desportos",)


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ("campo", "user", "data", "hora_inicio", "estado")
    list_filter = ("estado", "data")
    search_fields = ("campo__nome", "user__username")
    readonly_fields = ("criada_em",)
