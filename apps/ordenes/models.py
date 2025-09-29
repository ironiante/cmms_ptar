from django.db import models
from apps.equipos.models import Equipo
from apps.usuarios.models import User, Personal

class OrdenTrabajo(models.Model):
    TIPO_CHOICES = [
        ('PREVENTIVO', 'Preventivo'),
        ('CORRECTIVO', 'Correctivo'),
        ('PREDICTIVO', 'Predictivo'),
        ('EMERGENCIA', 'Emergencia'),
    ]

    ESTADO_CHOICES = [
        ('ABIERTA', 'Abierta'),
        ('EN_EJECUCION', 'En ejecución'),
        ('CERRADA', 'Cerrada'),
    ]

    PRIORIDAD_CHOICES = [
        ('ALTA', 'Alta'),
        ('MEDIA', 'Media'),
        ('BAJA', 'Baja'),
    ]

    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descripcion = models.TextField()
    prioridad = models.CharField(max_length=20, choices=PRIORIDAD_CHOICES, default='MEDIA')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ABIERTA')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_programada = models.DateTimeField(blank=True, null=True)
    fecha_cierre = models.DateTimeField(blank=True, null=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='ots_creadas')
    aprobado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='ots_aprobadas', blank=True)
    ejecutado_por = models.ForeignKey(Personal, on_delete=models.SET_NULL, null=True, related_name='ots_ejecutadas', blank=True)
    observaciones = models.TextField(blank=True)
    costo_estimado = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    costo_real = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"OT {self.id} - {self.equipo.nombre} ({self.estado})"
from django.db import models

# Create your models here.
