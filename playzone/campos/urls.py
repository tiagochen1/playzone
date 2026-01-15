from django.urls import path

from . import views
from . import admin_views

app_name = "campos"

urlpatterns = [
    # USER
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

    # ADMIN CUSTOM
    path("admin-dashboard/", admin_views.admin_dashboard, name="admin_dashboard"),
    path("admin/campos/", admin_views.admin_campos_list, name="admin_campos_list"),
    path("admin/campos/novo/", admin_views.admin_campo_create, name="admin_campo_create"),
    path("admin/campos/<int:campo_id>/editar/", admin_views.admin_campo_edit, name="admin_campo_edit"),
]
