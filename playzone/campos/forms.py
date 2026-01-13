from __future__ import annotations

from django import forms

from .models import Reserva
from .services import (
    validar_campo_disponivel,
    validar_conflito_reservas,
)


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ["data", "hora_inicio", "duracao_horas"]

    def __init__(self, *args, campo=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.campo = campo

    def clean(self):
        cleaned = super().clean()

        if not self.campo:
            return cleaned

        validar_campo_disponivel(self.campo)

        validar_conflito_reservas(
            campo=self.campo,
            data=cleaned.get("data"),
            hora_inicio=cleaned.get("hora_inicio"),
            duracao_horas=cleaned.get("duracao_horas"),
        )

        return cleaned
