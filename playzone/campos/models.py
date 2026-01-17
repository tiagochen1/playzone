from __future__ import annotations

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Desporto(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Desporto"
        verbose_name_plural = "Desportos"

    def __str__(self) -> str:
        return self.nome


class Campo(models.Model):
    class Estado(models.TextChoices):
        DISPONIVEL = "DISPONIVEL", "Disponível"
        MANUTENCAO = "MANUTENCAO", "Em Manutenção"
        INATIVO = "INATIVO", "Inativo"

    nome = models.CharField(max_length=100)
    preco_hora = models.DecimalField(max_digits=6, decimal_places=2)
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.DISPONIVEL,
    )
    desportos = models.ManyToManyField(Desporto, related_name="campos")
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Campo"
        verbose_name_plural = "Campos"

    def __str__(self) -> str:
        return self.nome


class Reserva(models.Model):
    class Estado(models.TextChoices):
        RESERVADA = "RESERVADA", "Reservada"
        CANCELADA = "CANCELADA", "Cancelada"
        CONCLUIDA = "CONCLUIDA", "Concluída"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservas",
    )
    campo = models.ForeignKey(
        Campo,
        on_delete=models.PROTECT,
        related_name="reservas",
    )
    data = models.DateField()
    hora_inicio = models.TimeField()
    duracao_horas = models.PositiveSmallIntegerField(default=1)
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.RESERVADA,
    )
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ["-data", "-hora_inicio"]

    def __str__(self) -> str:
        return f"{self.campo} - {self.data} {self.hora_inicio}"

    #REGRA DE NEGÓCIO 1: não permitir datas no passado
        # REGRA DE NEGÓCIO 1: não permitir datas no passado
    def clean(self):
        dt = timezone.datetime.combine(self.data, self.hora_inicio)

        # garantir timezone-aware (USE_TZ=True)
        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt, timezone.get_current_timezone())

        if dt < timezone.now():
            raise ValidationError("Não é possível reservar no passado.")

    @property
    def preco_total(self):
        return self.duracao_horas * self.campo.preco_hora
