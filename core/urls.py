from django.urls import path
from .views import index, reserve, reserve_process, unreserve_process

urlpatterns = [
    path('', index, name="index"),
    path('reserve', reserve, name='reserve'),
    path('reserve/new', reserve_process, name="reserve_process"),
    path('reserve/delete', unreserve_process, name="unreserve_process"),

]
