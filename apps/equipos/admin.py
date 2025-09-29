from django.contrib import admin
from .models import Equipo

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'zona', 'ubicacion', 'tag', 'especialidad', 'criticidad')
    search_fields = ('nombre', 'tag', 'zona')
    list_filter = ('especialidad', 'criticidad')
