from django.contrib import admin
from .models import Vehiculo, Solicitud

# Register your models here.
admin.site.register(Solicitud)

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ['marca', 'modelo', 'año', 'precio', 'estado', 'activo']
    list_filter = ['estado', 'activo', 'tipo']
    search_fields = ['marca', 'modelo']
    fields = ['marca', 'modelo', 'año', 'precio', 'estado', 'activo', 'tipo', 'descripcion', 'imagen', 'vendedor']