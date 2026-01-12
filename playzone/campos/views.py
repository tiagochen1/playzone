from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from .models import Campo


class CampoListView(ListView):
    model = Campo
    template_name = "campos/lista_campos.html"
    context_object_name = "campos"

class CampoReservaView (LoginRequiredMixin, DetailView):
    model= Campo
    template_name= "campos/reservar.html"


