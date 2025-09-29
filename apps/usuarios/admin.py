from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Rol', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'role')}),
    )
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff')
    search_fields = ('username', 'email')

    from .models import Personal

    @admin.register(Personal)
    class PersonalAdmin(admin.ModelAdmin):
        list_display = ('nombre', 'especialidad', 'nivel', 'documento', 'usuario')
        search_fields = ('nombre', 'documento')
from .models import RegistroHoras

@admin.register(RegistroHoras)
class RegistroHorasAdmin(admin.ModelAdmin):
    list_display = ('personal', 'fecha', 'horas')
    list_filter = ('fecha', 'personal')
    search_fields = ('personal__nombre',)


from django.contrib import admin

# Register your models here.
