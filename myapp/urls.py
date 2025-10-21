from django.urls import path, include
from rest_framework import routers
from .views import VehiculoViewSet, SolicitudViewSet

router = routers.DefaultRouter()
router.register(r'vehiculos', VehiculoViewSet)
router.register(r'solicitudes', SolicitudViewSet)

urlpatterns = [
    path('', include(router.urls)),
]