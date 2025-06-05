from rest_framework import viewsets
from .models import Usuario
from .serializer import UsuarioSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

class UsuarioView(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
class RegistroView(APIView):
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'mensaje': 'Usuario creado exitosamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            response = JsonResponse({'mensaje': 'Inicio de sesión exitoso'})
            response.set_cookie('sessionid', request.session.session_key)
            return response
        return JsonResponse({'error': 'Credenciales inválidas'}, status=400)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        response = JsonResponse({'mensaje': 'Sesión cerrada'})
        response.delete_cookie('sessionid')
        return response
    
class VistaProtegida(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'mensaje': f'Hola {request.user.email}, estás autenticado!'})
    


