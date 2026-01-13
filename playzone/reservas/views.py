from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def minhas_reservas(request):
    return render(request, "reservas/minhas_reservas.html")
