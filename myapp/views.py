from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Vehiculo, Solicitud
from .serializer import VehiculoSerializer, SolicitudSerializer

# 🔐 Permiso personalizado: solo el vendedor o un admin puede modificar/eliminar
class IsVendedorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.vendedor or request.user.is_staff or request.user.is_superuser

# 🚗 ViewSet de vehículos
class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

    def get_queryset(self):
        if self.action == 'list':
            return Vehiculo.objects.filter(activo=True)
        return Vehiculo.objects.all()


    def perform_create(self, serializer):
        serializer.save(vendedor=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsVendedorOrAdmin()]
        return [permissions.IsAuthenticatedOrReadOnly()]

# 📩 ViewSet de solicitudes
class SolicitudViewSet(viewsets.ModelViewSet):
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Solicitud.objects.all()
        return Solicitud.objects.filter(
            Q(solicitante=user) | Q(vehiculo__vendedor=user)
        )

    def perform_create(self, serializer):
        serializer.save(solicitante=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticatedOrReadOnly()]