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
            'rol': {'read_only': True},
        }

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("La contraseña debe tener al menos 6 caracteres.")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = Usuario(**validated_data)
        user.set_password(password)  # ✅ encripta la contraseña
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
            validated_data.pop('password')
        return super().update(instance, validated_data)