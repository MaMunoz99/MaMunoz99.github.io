from django.urls import path
from . import views

urlpatterns = [
    path('', views.mapa_view, name='mapa_view'),
    path('api/pines/', views.api_pines, name='api_pines'),
    path('api/crear_pin/', views.api_crear_pin, name='api_crear_pin'),
    path('api/estado_actual/', views.api_estado_actual, name='api_estado_actual'),
    path('api/historial_camara/<int:camara_id>/', views.api_historial_camara, name='api_historial_camara'),
]
