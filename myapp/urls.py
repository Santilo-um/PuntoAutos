from django.urls import path, include
from rest_framework import routers
from .views import VehiculoViewSet, SolicitudViewSet
from .views import aceptar_solicitud, rechazar_solicitud


router = routers.DefaultRouter()
router.register(r'vehiculos', VehiculoViewSet)
router.register(r'solicitudes', SolicitudViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('solicitud/<int:pk>/aceptar/', aceptar_solicitud, name='aceptar_solicitud'),
    path('solicitud/<int:pk>/rechazar/', rechazar_solicitud, name='rechazar_solicitud'),
]