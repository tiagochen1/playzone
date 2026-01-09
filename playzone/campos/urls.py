from django.urls import path
from .views import CampoListView

app_name = "campos"

urlpatterns = [
    path("", CampoListView.as_view(), name="list"),
]
