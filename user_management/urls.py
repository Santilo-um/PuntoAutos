from django.urls import path, include
from .views import RegistroView, LoginView, LogoutView, VistaProtegida

urlpatterns = [
    path('registro/', RegistroView.as_view(), name='registro'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('protegida/', VistaProtegida.as_view(), name='vista_protegida'),
]