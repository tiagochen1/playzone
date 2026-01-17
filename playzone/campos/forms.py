from __future__ import annotations

from django import forms

from .models import Campo, Reserva
from .services import validar_campo_disponivel, validar_conflito_reservas


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ["data", "hora_inicio", "duracao_horas"]

        widgets = {
            "data": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "hora_inicio": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "duracao_horas": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 8}),
        }

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


class CampoForm(forms.ModelForm):
    class Meta:
        model = Campo
        fields = ["nome", "desportos", "preco_hora", "estado"]

        widgets = {
            "nome": forms.TextInput(attrs={"class": "input", "placeholder": "Nome do Campo"}),
            "desportos": forms.SelectMultiple(attrs={"class": "select", "size": 3}),
            "preco_hora": forms.NumberInput(
                attrs={"class": "input", "step": "0.01", "min": "0", "placeholder": "Preço/hora"}
            ),
            "estado": forms.Select(attrs={"class": "select"}),
        }
