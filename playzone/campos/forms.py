from __future__ import annotations

import os
import uuid
from pathlib import Path

from django import forms
from django.conf import settings

from .models import Campo, Reserva
from .services import validar_campo_disponivel, validar_conflito_reservas


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ["data", "hora_inicio", "duracao_horas"]

        widgets = {
            # Alinhado com o design (Figma): usamos as classes do nosso CSS (main.css)
            "data": forms.DateInput(attrs={"class": "input", "type": "date"}),
            "hora_inicio": forms.TimeInput(attrs={"class": "input", "type": "time"}),
            "duracao_horas": forms.NumberInput(attrs={"class": "input", "min": 1, "max": 8}),
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
    # Upload opcional (guarda dentro de playzone/static/images/campos/ e coloca o caminho em Campo.foto)
    foto_upload = forms.ImageField(
        required=False,
        label="Imagem do campo",
        widget=forms.ClearableFileInput(
            attrs={
                "class": "input",
                "accept": "image/*",
            }
        ),
    )

    class Meta:
        model = Campo
        fields = ["nome", "desportos", "preco_hora", "estado", "foto"]

        widgets = {
            "nome": forms.TextInput(attrs={"class": "input", "placeholder": "Nome do Campo"}),
            "desportos": forms.SelectMultiple(attrs={"class": "select", "size": 3}),
            "preco_hora": forms.NumberInput(
                attrs={"class": "input", "step": "0.01", "min": "0", "placeholder": "Preço/hora"}
            ),
            "estado": forms.Select(attrs={"class": "select"}),
            "foto": forms.TextInput(
                attrs={
                    "class": "input",
                    "placeholder": "images/campos/desportivo-de-futebol.avif",
                }
            ),
        }

    def save(self, commit=True):
        instance: Campo = super().save(commit=False)

        upload = self.files.get("foto_upload")
        if upload:
            # Guardar dentro do static do projeto para ser servido como {%% static campo.foto %%}
            static_dir = Path(settings.BASE_DIR) / "playzone" / "static" / "images" / "campos"
            static_dir.mkdir(parents=True, exist_ok=True)

            ext = os.path.splitext(upload.name)[1].lower() or ".jpg"
            filename = f"campo_{uuid.uuid4().hex}{ext}"
            dest = static_dir / filename

            with open(dest, "wb") as f:
                for chunk in upload.chunks():
                    f.write(chunk)

            instance.foto = f"images/campos/{filename}"

        if commit:
            instance.save()
            self.save_m2m()
        return instance
