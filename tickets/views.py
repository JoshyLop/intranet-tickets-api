from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Ticket
from .serializers import TicketSerializer


class TicketViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar tickets.
    Proporciona operaciones CRUD completas para tickets.
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['titulo', 'descripcion']
    ordering_fields = ['creado_en', 'actualizado_en', 'prioridad']
    ordering = ['-creado_en']
    
    def get_queryset(self):
        """
        Filtra los tickets según parámetros de query.
        - mis_tickets: muestra solo los tickets del usuario actual
        - estado: filtra por estado
        - prioridad: filtra por prioridad
        - usuario: filtra por ID de usuario
        """
        queryset = super().get_queryset()
        
        # Filtrar por tickets del usuario actual
        mis_tickets = self.request.query_params.get('mis_tickets', None)
        if mis_tickets is not None and mis_tickets.lower() in ['true', '1', 'yes']:
            queryset = queryset.filter(usuario=self.request.user)
        
        # Filtrar por estado
        estado = self.request.query_params.get('estado', None)
        if estado is not None:
            queryset = queryset.filter(estado=estado)
        
        # Filtrar por prioridad
        prioridad = self.request.query_params.get('prioridad', None)
        if prioridad is not None:
            queryset = queryset.filter(prioridad=prioridad)
        
        # Filtrar por usuario
        usuario = self.request.query_params.get('usuario', None)
        if usuario is not None:
            queryset = queryset.filter(usuario__id=usuario)
        
        return queryset
