from django.urls import path
from . import views

urlpatterns = [
    path('', views.mapa_view, name='mapa_view'),
    path('api/pines/', views.api_pines, name='api_pines'),
    path('api/crear_pin/', views.api_crear_pin, name='api_crear_pin'),
]
