from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .models import Usuario
from .serializer import UsuarioSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from myapp.models import Vehiculo, Solicitud
from myapp.serializer import VehiculoSerializer, SolicitudSerializer

class UsuarioView(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

class RegistroView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'mensaje': 'Usuario creado exitosamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'nombre': user.nombre,
                    'rol': user.rol
                }
            })
        return Response({'error': 'Credenciales inválidas'}, status=401)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return JsonResponse({'mensaje': 'Sesión cerrada'})

class VistaProtegida(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'mensaje': f'Hola {request.user.email}, estás autenticado!'})
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def perfil_usuario(request):
    usuario = request.user

    publicaciones = usuario.vehiculos.all()
    solicitudes_realizadas = usuario.solicitudes.all()
    solicitudes_recibidas = Solicitud.objects.filter(vehiculo__vendedor=usuario)

    return Response({
        "usuario": {
            "id": usuario.id,
            "email": usuario.email,
        },
        "publicaciones": VehiculoSerializer(publicaciones, many=True).data,
        "solicitudes_realizadas": SolicitudSerializer(solicitudes_realizadas, many=True).data,
        "solicitudes_recibidas": SolicitudSerializer(solicitudes_recibidas, many=True).data,
    })
    


