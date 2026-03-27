from django.contrib import admin
from .models import Camion, Camara, Deteccion

@admin.register(Camara)
class CamaraAdmin(admin.ModelAdmin):
    list_display = ('id', 'lat', 'long', 'estado')
    list_filter = ('estado',)

@admin.register(Camion)
class CamionAdmin(admin.ModelAdmin):
    list_display = ('id', 'patente', 'id_frame')
    search_fields = ('patente', 'id_frame')

@admin.register(Deteccion)
class DeteccionAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_camion', 'id_camara', 'fecha')
    list_filter = ('id_camara', 'fecha')
    date_hierarchy = 'fecha'
