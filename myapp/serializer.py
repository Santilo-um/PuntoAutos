from rest_framework import serializers
from .models import Vehiculo, Solicitud
from user_management.models import Usuario

class VehiculoSerializer(serializers.ModelSerializer):
    vendedor = serializers.ReadOnlyField(source='vendedor.email')
    imagen = serializers.ImageField(required=False)

    class Meta:
        model = Vehiculo
        fields = '__all__'
        read_only_fields = ['vendedor', 'fecha_publicacion']

    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a cero.")
        return value

class SolicitudSerializer(serializers.ModelSerializer):
    solicitante = serializers.ReadOnlyField(source='solicitante.email')
    vehiculo = serializers.PrimaryKeyRelatedField(queryset=Vehiculo.objects.filter(estado='disponible'))

    class Meta:
        model = Solicitud
        fields = '__all__'
        read_only_fields = ['solicitante', 'fecha']


    def validate(self, data):
        solicitante = self.context['request'].user
        vehiculo = data['vehiculo']

        if vehiculo.vendedor == solicitante:
            raise serializers.ValidationError("No puedes solicitar tu propio vehículo.")

        if Solicitud.objects.filter(solicitante=solicitante, vehiculo=vehiculo).exists():
            raise serializers.ValidationError("Ya enviaste una solicitud para este vehículo.")

        return data

    def update(self, instance, validated_data):
        estado_nuevo = validated_data.get('estado', instance.estado)

        if instance.estado != 'aceptada' and estado_nuevo == 'aceptada':
            vehiculo = instance.vehiculo
            vehiculo.estado = 'vendido'
            vehiculo.save()

        instance.estado = estado_nuevo
        instance.save()
        return instance