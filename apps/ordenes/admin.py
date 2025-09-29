from django.contrib import admin
from .models import OrdenTrabajo

@admin.register(OrdenTrabajo)
class OrdenTrabajoAdmin(admin.ModelAdmin):
    list_display = ('id', 'equipo', 'tipo', 'prioridad', 'estado', 'fecha_creacion', 'fecha_programada')
    list_filter = ('tipo', 'estado', 'prioridad', 'fecha_creacion')
    search_fields = ('equipo__nombre', 'descripcion')
from .models import PlanMantenimiento

@admin.register(PlanMantenimiento)
class PlanMantenimientoAdmin(admin.ModelAdmin):
    list_display = ('equipo', 'tipo', 'frecuencia', 'activo', 'creado_en')
    list_filter = ('tipo', 'frecuencia', 'activo')
    search_fields = ('equipo__nombre', 'descripcion')

from .models import Repuesto, UsoRepuesto, MovInventario

@admin.register(Repuesto)
class RepuestoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'stock', 'stock_minimo', 'especialidad')
    search_fields = ('codigo', 'nombre')
    list_filter = ('especialidad',)

@admin.register(UsoRepuesto)
class UsoRepuestoAdmin(admin.ModelAdmin):
    list_display = ('orden', 'repuesto', 'cantidad', 'fecha')
    list_filter = ('fecha',)

@admin.register(MovInventario)
class MovInventarioAdmin(admin.ModelAdmin):
    list_display = ('repuesto', 'tipo', 'cantidad', 'fecha', 'usuario')
    list_filter = ('tipo', 'fecha')
from .models import Evidencia, HistorialOT

@admin.register(Evidencia)
class EvidenciaAdmin(admin.ModelAdmin):
    list_display = ('orden', 'tipo', 'fecha_subida')
    list_filter = ('tipo', 'fecha_subida')
    search_fields = ('orden__id',)

@admin.register(HistorialOT)
class HistorialOTAdmin(admin.ModelAdmin):
    list_display = ('orden', 'costo_total', 'mtbf', 'mttr', 'fecha_registro')
    search_fields = ('orden__id',)
from .models import AnalisisRCM, FMEA_Detalle

@admin.register(AnalisisRCM)
class AnalisisRCMAdmin(admin.ModelAdmin):
    list_display = ('equipo', 'criticidad', 'rpn', 'fecha_analisis', 'responsable')
    list_filter = ('criticidad', 'fecha_analisis')
    search_fields = ('equipo__nombre',)

@admin.register(FMEA_Detalle)
class FMEADetalleAdmin(admin.ModelAdmin):
    list_display = ('rcm', 'modo_falla', 'severidad', 'ocurrencia', 'deteccion', 'rpn')
    list_filter = ('severidad', 'ocurrencia', 'deteccion')
    search_fields = ('modo_falla', 'causa', 'efecto')

from django.contrib import admin

# Register your models here.
