from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Ticket


class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo User (datos básicos).
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class TicketSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Ticket.
    """
    usuario_detalle = UsuarioSerializer(source='usuario', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    prioridad_display = serializers.CharField(source='get_prioridad_display', read_only=True)
    
    class Meta:
        model = Ticket
        fields = [
            'id',
            'titulo',
            'descripcion',
            'estado',
            'estado_display',
            'prioridad',
            'prioridad_display',
            'usuario',
            'usuario_detalle',
            'creado_en',
            'actualizado_en',
        ]
        read_only_fields = ['id', 'creado_en', 'actualizado_en', 'usuario_detalle', 'estado_display', 'prioridad_display']
    
    def create(self, validated_data):
        """
        Asigna automáticamente el usuario autenticado al crear un ticket.
        """
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['usuario'] = request.user
        return super().create(validated_data)
