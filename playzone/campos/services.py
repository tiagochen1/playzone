from __future__ import annotations

from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Campo, Reserva


# REGRA 2: campo tem de estar disponível
def validar_campo_disponivel(campo: Campo):
    if campo.estado != Campo.Estado.DISPONIVEL:
        raise ValidationError("Este campo não está disponível para reservas.")


# REGRA 3: não permitir reservas sobrepostas
def validar_conflito_reservas(
    campo: Campo,
    data,
    hora_inicio,
    duracao_horas,
):
    inicio = datetime.combine(data, hora_inicio)
    fim = inicio + timedelta(hours=duracao_horas)

    conflitos = Reserva.objects.filter(
        campo=campo,
        data=data,
        estado=Reserva.Estado.RESERVADA,
    )

    for r in conflitos:
        r_inicio = datetime.combine(r.data, r.hora_inicio)
        r_fim = r_inicio + timedelta(hours=r.duracao_horas)

        if inicio < r_fim and fim > r_inicio:
            raise ValidationError("Já existe uma reserva neste horário.")


# REGRA 4: cancelamento só até X horas antes
def pode_cancelar(reserva: Reserva, horas_limite: int = 2) -> bool:
    """Permitir cancelar apenas até `horas_limite` horas antes do início.

    `timezone.now()` é *aware* quando USE_TZ=True. Como `datetime.combine()` cria
    um datetime *naive*, temos de o tornar *aware* para evitar:
    "can't compare offset-naive and offset-aware datetimes".
    """

    inicio = datetime.combine(reserva.data, reserva.hora_inicio)
    if timezone.is_naive(inicio):
        inicio = timezone.make_aware(inicio, timezone.get_current_timezone())

    limite = inicio - timedelta(hours=horas_limite)
    return timezone.now() < limite


# REGRA 5: receita mensal (admin dashboard)
def receita_mes_atual() -> float:
    agora = timezone.now()
    reservas = Reserva.objects.filter(
        estado=Reserva.Estado.RESERVADA,
        data__year=agora.year,
        data__month=agora.month,
    )
    return float(sum(r.preco_total for r in reservas))


def reservas_hoje() -> int:
    hoje = timezone.localdate()
    return Reserva.objects.filter(
        data=hoje,
        estado=Reserva.Estado.RESERVADA,
    ).count()


def campos_disponiveis_ratio() -> tuple[int, int]:
    total = Campo.objects.count()
    disponiveis = Campo.objects.filter(estado=Campo.Estado.DISPONIVEL).count()
    return disponiveis, total
