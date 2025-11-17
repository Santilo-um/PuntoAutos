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
from rest_framework_simplejwt.authentication import JWTAuthentication


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


class PerfilView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Vehículos publicados por este usuario
        publicaciones = Vehiculo.objects.filter(vendedor=user)

        publicaciones_data = []
        for v in publicaciones:
            publicaciones_data.append({
                "vehiculo_id": v.id,
                "marca": v.marca,
                "modelo": v.modelo,
                "precio": float(v.precio),
                "estado": v.estado,
                "solicitudes": [
                    {
                        "id": s.id,
                        "estado": s.estado,
                        "mensaje": s.mensaje,
                        "fecha_solicitud": s.fecha_solicitud,
                        "solicitante": {
                            "id": s.solicitante.id,
                            "email": s.solicitante.email,
                            "telefono": s.solicitante.telefono,
                        }
                    }
                    for s in v.solicitudes.all()
                ]
            })

        # Solicitudes enviadas por este usuario
        solicitudes_enviadas = Solicitud.objects.filter(solicitante=user)

        solicitudes_enviadas_data = [
            {
                "id": s.id,
                "estado": s.estado,
                "mensaje": s.mensaje,
                "vehiculo": {
                    "id": s.vehiculo.id,
                    "marca": s.vehiculo.marca,
                    "modelo": s.vehiculo.modelo,
                },
                "fecha_solicitud": s.fecha_solicitud,
            }
            for s in solicitudes_enviadas
        ]

        return Response({
            "usuario": {
                "id": user.id,
                "email": user.email
            },
            "publicaciones": publicaciones_data,
            "solicitudes_enviadas": solicitudes_enviadas_data
        })

class ActualizarTelefonoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        telefono = request.data.get("telefono")

        if telefono is None:
            return Response({"error": "Debes enviar un teléfono"}, status=400)

        request.user.telefono = telefono
        request.user.save()

        return Response({"mensaje": "Teléfono actualizado correctamente"})
    