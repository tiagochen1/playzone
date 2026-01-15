from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReservaForm
from .models import Campo, Reserva
from .services import pode_cancelar


@login_required
def campos_list(request):
    campos = Campo.objects.prefetch_related("desportos").all()
    return render(
        request,
        "campos/user_campos_list.html",
        {"campos": campos},
    )


@login_required
def reservar_campo(request, campo_id: int):
    campo = get_object_or_404(Campo, pk=campo_id)

    if request.method == "POST":
        form = ReservaForm(request.POST, campo=campo)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.user = request.user
            reserva.campo = campo
            reserva.save()
            messages.success(request, "Reserva efetuada com sucesso.")
            return redirect("campos:minhas_reservas")
    else:
        form = ReservaForm(campo=campo)

    return render(
        request,
        "campos/user_reservar.html",
        {
            "campo": campo,
            "form": form,
        },
    )


@login_required
def minhas_reservas(request):
    reservas = Reserva.objects.filter(
        user=request.user,
        estado=Reserva.Estado.RESERVADA,
    ).select_related("campo")

    return render(
        request,
        "campos/user_minhas_reservas.html",
        {"reservas": reservas},
    )


@login_required
def cancelar_reserva(request, reserva_id: int):
    reserva = get_object_or_404(
        Reserva,
        pk=reserva_id,
        user=request.user,
        estado=Reserva.Estado.RESERVADA,
    )

    if not pode_cancelar(reserva):
        messages.error(request, "Já não é possível cancelar esta reserva.")
        return redirect("campos:minhas_reservas")

    reserva.estado = Reserva.Estado.CANCELADA
    reserva.save()
    messages.success(request, "Reserva cancelada.")
    return redirect("campos:minhas_reservas")


@login_required
def historico(request):
    reservas = Reserva.objects.filter(
        user=request.user,
    ).exclude(
        estado=Reserva.Estado.RESERVADA,
    ).select_related("campo")

    return render(
        request,
        "campos/user_historico.html",
        {"reservas": reservas},
    )
