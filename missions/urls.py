from django.urls import path

from . import views

app_name = "missions"

urlpatterns = [
    path('', views.index, name="index"),
]