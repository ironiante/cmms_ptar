from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)

    ROLE_CHOICES = [
        ('GERENTE', 'Gerente de Mantenimiento'),
        ('ING', 'Ingeniero Profesional'),
        ('COORD', 'Coordinador de Mantenimiento'),
        ('JEFE_TURNO', 'Jefe de Turno'),
        ('TEC_MEC_N2', 'Técnico N2 Mecánico'),
        ('TEC_ELEC_N2', 'Técnico N2 Eléctrico'),
        ('TEC_INST_N2', 'Técnico N2 Instrumentación'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='COORD')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
class Personal(models.Model):
    nombre = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='personal_fotos/', blank=True, null=True)
    especialidad = models.CharField(
        max_length=50,
        choices=[
            ('MECANICO', 'Mecánico'),
            ('ELECTRICO', 'Eléctrico'),
            ('INSTRUMENTACION', 'Instrumentación'),
        ]
    )
    nivel = models.IntegerField(help_text="Nivel 1 o 2")
    documento = models.CharField(max_length=50, unique=True)
    contacto = models.CharField(max_length=100)
    usuario = models.OneToOneField(
        'usuarios.User',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        help_text="Solo para personal que tiene cuenta de usuario"
    )

    def __str__(self):
        return f"{self.nombre} ({self.especialidad})"
class RegistroHoras(models.Model):
    personal = models.ForeignKey(
        'usuarios.Personal',
        on_delete=models.CASCADE,
        related_name='registros_horas'
    )
    fecha = models.DateField(auto_now_add=True)
    horas = models.DecimalField(max_digits=5, decimal_places=2, help_text="Horas trabajadas en el día")
    descripcion = models.TextField(blank=True, help_text="Descripción de la actividad realizada")

    def __str__(self):
        return f"{self.personal.nombre} - {self.fecha} ({self.horas} h)"
