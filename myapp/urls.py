from django.urls import path, include 
from rest_framework import routers
from .views import UsuarioView, VehiculoView, SolcitudesView

router = routers.DefaultRouter()
router.register(r'Usuarios', UsuarioView)
router.register(r'Vehiculos', VehiculoView)
router.register(r'Solicitudes', SolcitudesView)

urlpatterns = [
    path('', include(router.urls))
]