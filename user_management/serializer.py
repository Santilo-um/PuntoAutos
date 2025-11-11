from rest_framework import serializers
from .models import Usuario
from django.contrib.auth.hashers import make_password

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'email', 'nombre', 'telefono', 'password', 'rol']
        extra_kwargs = {
            'password': {'write_only': True},
            'nombre': {'required': False},
            'telefono': {'required': False},
            'rol': {'read_only': True},  # Evita que el usuario se asigne rol manualmente
        }
        

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("La contraseña debe tener al menos 6 caracteres.")
        return value

    def create(self, validated_data):
        return Usuario.objects.create_user(**validated_data)
    