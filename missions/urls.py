from django.urls import path

from . import views

app_name = "missions"

urlpatterns = [
    path('', views.get_mission, name="get"),
    path('<int:year>/<int:month>/<int:day>/', views.get_mission, name="get_archive"),
    path('list/', views.list_missions, name="list"),
]