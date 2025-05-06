from django.urls import path, include 
from rest_framework import routers
from .views import UsuarioView, VehiculoView, SolcitudesView, LoginView, LogoutView

router = routers.DefaultRouter()
router.register(r'Usuarios', UsuarioView)
router.register(r'Vehiculos', VehiculoView)
router.register(r'Solicitudes', SolcitudesView)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
]