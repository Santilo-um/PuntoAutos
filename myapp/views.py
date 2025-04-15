from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .serializer import *
from .models import *

class UsuarioView(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer
    queryset = Usuario.objects.all()

class VehiculoView(viewsets.ModelViewSet):
    serializer_class = VehiculoSerializer
    queryset = Vehiculo.objects.all()
    
class SolcitudesView(viewsets.ModelViewSet):
    serializer_class = SolicitudesSerializer
    queryset = Solicitudes.objects.all()
    