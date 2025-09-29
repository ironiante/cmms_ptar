from django.contrib import admin
from .models import OrdenTrabajo

@admin.register(OrdenTrabajo)
class OrdenTrabajoAdmin(admin.ModelAdmin):
    list_display = ('id', 'equipo', 'tipo', 'prioridad', 'estado', 'fecha_creacion', 'fecha_programada')
    list_filter = ('tipo', 'estado', 'prioridad', 'fecha_creacion')
    search_fields = ('equipo__nombre', 'descripcion')
from django.contrib import admin

# Register your models here.
