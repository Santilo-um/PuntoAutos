from django.db import models

# Create your models here.

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return self.nombre
    
class Vehiculo(models.Model):
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    año = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    km = models.IntegerField()
    tipo = models.CharField(max_length=10)
    color = models.CharField(max_length=10)
    estado = models.CharField(max_length=10)
    descripcion = models.TextField(blank=True, null=True)
    fecha_publicacion = models.DateTimeField()

    def __str__(self):
        return self.modelo
    
class Solicitudes(models.Model):
    mensaje = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=10)
    fecha_solicitud = models.DateTimeField()

    def __str__(self):
        return self.mensaje