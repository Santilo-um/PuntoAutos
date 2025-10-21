from rest_framework import viewsets, permissions
from .models import Vehiculo, Solicitud
from .serializer import VehiculoSerializer, SolicitudSerializer

# Permiso personalizado: solo el vendedor o un admin puede modificar/eliminar
class IsVendedorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.vendedor or request.user.is_staff or request.user.is_superuser


class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

    def perform_create(self, serializer):
        serializer.save(vendedor=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsVendedorOrAdmin()]
        return [permissions.IsAuthenticatedOrReadOnly()]

class SolicitudViewSet(viewsets.ModelViewSet):
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Solicitud.objects.all()
        return Solicitud.objects.filter(solicitante=user) | Solicitud.objects.filter(vehiculo__vendedor=user)

    def perform_create(self, serializer):
        serializer.save(solicitante=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticatedOrReadOnly()]
    