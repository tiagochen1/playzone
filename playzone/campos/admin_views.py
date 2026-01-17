from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CampoForm
from .models import Campo, Desporto, Reserva
from .permissions import ensure_admin_group_exists, is_admin
from .services import campos_disponiveis_ratio, receita_mes_atual, reservas_hoje


def admin_required(view_func):
    return login_required(user_passes_test(is_admin)(view_func))


@admin_required
def admin_dashboard(request):
    ensure_admin_group_exists()

    # Criar desporto diretamente no dashboard
    if request.method == "POST":
        nome = (request.POST.get("desporto_nome") or "").strip()
        if not nome:
            messages.error(request, "Indica o nome do desporto.")
            return redirect("campos:admin_dashboard")
        # evitar duplicados (case-insensitive)
        if Desporto.objects.filter(nome__iexact=nome).exists():
            messages.error(request, "Esse desporto já existe.")
            return redirect("campos:admin_dashboard")
        Desporto.objects.create(nome=nome)
        messages.success(request, "Desporto adicionado com sucesso.")
        return redirect("campos:admin_dashboard")

    kpi_reservas_hoje = reservas_hoje()
    disp, total = campos_disponiveis_ratio()
    kpi_campos_disp = f"{disp}/{total}"
    kpi_receita_mes = receita_mes_atual()

    # tabela de reservas (últimas 12)
    ultimas = (
        Reserva.objects.select_related("campo", "user")
        .order_by("-data", "-hora_inicio")[:12]
    )

    desportos = Desporto.objects.all().order_by("nome")

    return render(
        request,
        "campos/admin_dashboard.html",
        {
            "kpi_reservas_hoje": kpi_reservas_hoje,
            "kpi_campos_disp": kpi_campos_disp,
            "kpi_receita_mes": kpi_receita_mes,
            "reservas": ultimas,
            "desportos": desportos,
        },
    )


@admin_required
def admin_campos_list(request):
    ensure_admin_group_exists()

    q = (request.GET.get("q") or "").strip()
    estado = (request.GET.get("estado") or "").strip()
    desporto_id = (request.GET.get("desporto") or "").strip()

    campos_qs = Campo.objects.prefetch_related("desportos").all()

    if q:
        campos_qs = campos_qs.filter(nome__icontains=q)
    if estado:
        campos_qs = campos_qs.filter(estado=estado)
    if desporto_id:
        campos_qs = campos_qs.filter(desportos__id=desporto_id)

    # para dropdown filtro
    desportos = Desporto.objects.all().order_by("nome")

    return render(
        request,
        "campos/admin_campos_list.html",
        {
            "campos": campos_qs.distinct(),
            "q": q,
            "estado": estado,
            "desporto_id": desporto_id,
            "desportos": desportos,
            "estados": Campo.Estado.choices,
        },
    )


@admin_required
def admin_campo_create(request):
    ensure_admin_group_exists()

    if request.method == "POST":
        form = CampoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Campo criado com sucesso.")
            return redirect("campos:admin_campos_list")
    else:
        form = CampoForm()

    return render(
        request,
        "campos/admin_campo_form.html",
        {"form": form, "modo": "criar"},
    )


@admin_required
def admin_campo_edit(request, campo_id: int):
    ensure_admin_group_exists()
    campo = get_object_or_404(Campo, pk=campo_id)

    if request.method == "POST":
        form = CampoForm(request.POST, request.FILES, instance=campo)
        if form.is_valid():
            form.save()
            messages.success(request, "Campo atualizado com sucesso.")
            return redirect("campos:admin_campos_list")
    else:
        form = CampoForm(instance=campo)

    return render(
        request,
        "campos/admin_campo_form.html",
        {"form": form, "modo": "editar", "campo": campo},
    )
