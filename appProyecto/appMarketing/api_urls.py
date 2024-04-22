from django.urls import path

from .api_views import *

urlpatterns = [
    path('servicios', servicio_list)
]