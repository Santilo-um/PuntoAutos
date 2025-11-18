from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Tipos de vehículo
TIPO_CHOICES = [
    ('auto', 'Auto'),
    ('moto', 'Moto'),
    ('camioneta', 'Camioneta'),
]

ESTADO_CHOICES = [
    ('disponible', 'Disponible'),
    ('vendido', 'Vendido'),
    ('pausado', 'Pausado'),
]

SOLICITUD_ESTADO_CHOICES = [
    ('pendiente', 'Pendiente'),
    ('aceptada', 'Aceptada'),
    ('rechazada', 'Rechazada'),
]

class Vehiculo(models.Model):
    activo = models.BooleanField(default=True)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    año = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2100)])
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    imagen = models.ImageField(upload_to='vehiculos/', null=True, blank=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='disponible')
    descripcion = models.TextField(blank=True, null=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    vendedor = models.ForeignKey('user_management.Usuario', on_delete=models.CASCADE, related_name='vehiculos')
    
    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.año})"

    def marcar_como_vendido(self):
        self.estado = 'vendido'
        self.save()

    def pausado(self):
        return self.estado == 'pausado'


class Solicitud(models.Model):
    mensaje = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=10, choices=SOLICITUD_ESTADO_CHOICES, default='pendiente')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='solicitudes')
    solicitante = models.ForeignKey('user_management.Usuario', on_delete=models.CASCADE, related_name='solicitudes')

    def __str__(self):
        return f"Solicitud de {self.solicitante.email} para {self.vehiculo.modelo}"

    def aceptar(self):
        self.estado = 'aceptada'
        self.save()
        self.vehiculo.marcar_como_vendido()

    def rechazar(self):
        self.estado = 'rechazada'
        self.save()