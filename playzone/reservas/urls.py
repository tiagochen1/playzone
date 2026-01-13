from django.urls import path
from .views import minhas_reservas

app_name = "reservas"

urlpatterns = [
    path("minhas/", minhas_reservas, name="minhas"),
]
