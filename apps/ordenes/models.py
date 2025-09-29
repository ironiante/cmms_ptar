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

from apps.equipos.models import Equipo
from apps.usuarios.models import User

class PlanMantenimiento(models.Model):
    TIPO_CHOICES = [
        ('PREVENTIVO', 'Preventivo'),
        ('PREDICTIVO', 'Predictivo'),
    ]

    FRECUENCIA_CHOICES = [
        ('SEMANAL', 'Semanal'),
        ('MENSUAL', 'Mensual'),
        ('TRIMESTRAL', 'Trimestral'),
        ('ANUAL', 'Anual'),
        ('HORAS', 'Por horas'),
        ('CONDICION', 'Por condición'),
    ]

    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='planes_mantenimiento')
    descripcion = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    frecuencia = models.CharField(max_length=20, choices=FRECUENCIA_CHOICES)
    condicion_umbral = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Sólo si es por condición: ej. vibración > x mm/s"
    )
    recursos_previstos = models.TextField(blank=True, null=True)
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='planes_responsable')
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Plan {self.id} - {self.equipo.nombre} ({self.tipo})"
class Repuesto(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    especialidad = models.CharField(
        max_length=50,
        choices=[
            ('MECANICO', 'Mecánico'),
            ('ELECTRICO', 'Eléctrico'),
            ('INSTRUMENTACION', 'Instrumentación'),
        ]
    )
    ubicacion = models.CharField(max_length=100)
    stock = models.IntegerField(default=0)
    unidad = models.CharField(max_length=20, default='unid')
    proveedor = models.CharField(max_length=100, blank=True, null=True)
    stock_minimo = models.IntegerField(default=0)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"


class UsoRepuesto(models.Model):
    orden = models.ForeignKey('ordenes.OrdenTrabajo', on_delete=models.CASCADE, related_name='usos_repuesto')
    repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.repuesto.nombre} usado en OT {self.orden.id}"


class MovInventario(models.Model):
    TIPO_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida'),
        ('AJUSTE', 'Ajuste'),
    ]
    repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE, related_name='movimientos')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey('usuarios.User', on_delete=models.SET_NULL, null=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.tipo} - {self.repuesto.nombre} ({self.cantidad})"
class Evidencia(models.Model):
    TIPO_CHOICES = [
        ('FOTO', 'Foto'),
        ('DOCUMENTO', 'Documento'),
        ('FIRMA', 'Firma'),
    ]
    orden = models.ForeignKey('ordenes.OrdenTrabajo', on_delete=models.CASCADE, related_name='evidencias')
    archivo = models.FileField(upload_to='evidencias/')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} - OT {self.orden.id}"


class HistorialOT(models.Model):
    orden = models.OneToOneField('ordenes.OrdenTrabajo', on_delete=models.CASCADE, related_name='historial')
    resumen = models.TextField(blank=True, null=True)
    costo_total = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    mtbf = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Tiempo medio entre fallas (horas)")
    mttr = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Tiempo medio de reparación (horas)")
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Historial OT {self.orden.id}"
class AnalisisRCM(models.Model):
    equipo = models.ForeignKey('equipos.Equipo', on_delete=models.CASCADE, related_name='analisis_rcm')
    criticidad = models.CharField(
        max_length=50,
        choices=[
            ('ALTA', 'Alta'),
            ('MEDIA', 'Media'),
            ('BAJA', 'Baja'),
        ]
    )
    rpn = models.IntegerField(help_text="Risk Priority Number calculado")
    fecha_analisis = models.DateField(auto_now_add=True)
    responsable = models.ForeignKey('usuarios.User', on_delete=models.SET_NULL, null=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"RCM {self.equipo.nombre} ({self.criticidad})"


class FMEA_Detalle(models.Model):
    rcm = models.ForeignKey(AnalisisRCM, on_delete=models.CASCADE, related_name='fmea_detalles')
    funcion = models.TextField()
    modo_falla = models.TextField()
    causa = models.TextField()
    efecto = models.TextField()
    severidad = models.IntegerField(help_text="1-10")
    ocurrencia = models.IntegerField(help_text="1-10")
    deteccion = models.IntegerField(help_text="1-10")
    rpn = models.IntegerField(help_text="S*O*D")

    def __str__(self):
        return f"FMEA {self.rcm.equipo.nombre} - {self.modo_falla}"

from django.db import models

# Create your models here.
