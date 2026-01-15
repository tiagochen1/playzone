from django.urls import path

from . import views

app_name = "campos"

urlpatterns = [
    path("", views.campos_list, name="campos_list"),
    path("campos/", views.campos_list, name="campos_list"),

    path("reservar/<int:campo_id>/", views.reservar_campo, name="reservar"),
    path("minhas-reservas/", views.minhas_reservas, name="minhas_reservas"),
    path(
        "minhas-reservas/<int:reserva_id>/cancelar/",
        views.cancelar_reserva,
        name="cancelar_reserva",
    ),
    path("historico/", views.historico, name="historico"),
]
