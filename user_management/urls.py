from django.urls import path, include
from .views import RegistroView, LoginView, LogoutView, VistaProtegida
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegistroView, LoginView, LogoutView, VistaProtegida, PerfilView, ActualizarTelefonoView


urlpatterns = [
    path('registro/', RegistroView.as_view(), name='registro'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('protegida/', VistaProtegida.as_view(), name='vista_protegida'),
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('perfil/', PerfilView.as_view(), name='perfil'),
    path('actualizar-telefono/', ActualizarTelefonoView.as_view(), name='actualizar-telefono'),




]

