from django.urls import path
from .views import CampoListView, CampoReservaView

app_name = "campos"

urlpatterns = [
    path("", CampoListView.as_view(), name="list"),
    path("reservar/<int:pk>/", CampoReservaView.as_view(), name="reservar"),
]
