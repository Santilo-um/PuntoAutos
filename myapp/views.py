from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from .models import Vehiculo, Solicitud
from .serializer import VehiculoSerializer, SolicitudSerializer
from rest_framework.exceptions import PermissionDenied


# 🔐 Permiso personalizado: solo el vendedor o un admin puede modificar/eliminar
class IsVendedorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.vendedor or 
            getattr(request.user, "is_admin", False) or 
            getattr(request.user, "is_superuser", False)
        )

# 🚗 ViewSet de vehículos
class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.action == 'list':
            return Vehiculo.objects.filter(activo=True)
        return Vehiculo.objects.all()

    def perform_create(self, serializer):
        serializer.save(vendedor=self.request.user)
        
    def perform_destroy(self, instance):
        user = self.request.user

        # Solo el dueño o el admin pueden eliminar
        if instance.vendedor != user and not getattr(user, "is_admin", False):
            raise PermissionDenied("No puedes eliminar un vehículo que no es tuyo.")

        return super().perform_destroy(instance)


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

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def aceptar_solicitud(request, pk):
    try:
        solicitud = Solicitud.objects.get(id=pk)
    except Solicitud.DoesNotExist:
        return Response({"error": "Solicitud no encontrada"}, status=404)

    # Solo el vendedor del vehículo puede aceptar
    if solicitud.vehiculo.vendedor != request.user:
        return Response({"error": "No autorizado"}, status=403)

    solicitud.estado = "aceptada"
    solicitud.save()

    return Response({
        "mensaje": "Solicitud aceptada correctamente",
        "solicitud_id": solicitud.id,
        "estado": solicitud.estado,
    }, status=200)


# -----------------------------
#  RECHAZAR SOLICITUD
# -----------------------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def rechazar_solicitud(request, pk):
    try:
        solicitud = Solicitud.objects.get(id=pk)
    except Solicitud.DoesNotExist:
        return Response({"error": "Solicitud no encontrada"}, status=404)

    # Solo el vendedor del vehículo puede rechazar
    if solicitud.vehiculo.vendedor != request.user:
        return Response({"error": "No autorizado"}, status=403)

    solicitud.estado = "rechazada"
    solicitud.save()

    return Response({
        "mensaje": "Solicitud rechazada correctamente",
        "solicitud_id": solicitud.id,
        "estado": solicitud.estado,
    }, status=200)