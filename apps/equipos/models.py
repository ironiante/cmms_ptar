from django.db import models

class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    zona = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    tag = models.CharField(max_length=50, unique=True, help_text="Código o identificación única")
    especialidad = models.CharField(
        max_length=50,
        choices=[
            ('MECANICO', 'Mecánico'),
            ('ELECTRICO', 'Eléctrico'),
            ('INSTRUMENTACION', 'Instrumentación'),
        ]
    )
    criticidad = models.CharField(
        max_length=50,
        choices=[
            ('ALTA', 'Alta'),
            ('MEDIA', 'Media'),
            ('BAJA', 'Baja'),
        ]
    )
    descripcion = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.tag})"
from django.db import models

# Create your models here.
