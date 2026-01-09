from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class CampoListView(LoginRequiredMixin, TemplateView):
    template_name = "campos/lista_campos.html"
