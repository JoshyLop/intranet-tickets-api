"""
Vistas (ViewSets) para la API REST del sistema de tickets.
Los ViewSets manejan las operaciones CRUD (Crear, Leer, Actualizar, Eliminar).
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from .models import Ticket, Comment, UserProfile
from .serializers import (
    TicketSerializer,
    TicketDetailSerializer,
    TicketCreateSerializer,
    TicketStatusUpdateSerializer,
    CommentSerializer,
    UserProfileSerializer,
    UserSerializer
)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet de solo lectura para usuarios.
    
    Endpoints:
    - GET /api/users/ - Lista todos los usuarios
    - GET /api/users/{id}/ - Detalle de un usuario específico
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['username', 'date_joined']
    ordering = ['username']


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet para perfiles de usuario.
    
    Endpoints:
    - GET /api/profiles/ - Lista todos los perfiles
    - POST /api/profiles/ - Crear nuevo perfil
    - GET /api/profiles/{id}/ - Detalle de un perfil
    - PUT /api/profiles/{id}/ - Actualizar perfil completo
    - PATCH /api/profiles/{id}/ - Actualizar perfil parcial
    - DELETE /api/profiles/{id}/ - Eliminar perfil (solo admin)
    """
    queryset = UserProfile.objects.select_related('user').all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_support_staff', 'department']
    search_fields = ['user__username', 'user__email', 'department', 'phone']
    ordering_fields = ['created_at', 'user__username']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'], url_path='me')
    def current_user_profile(self, request):
        """
        Endpoint personalizado para obtener el perfil del usuario actual.
        
        GET /api/profiles/me/
        """
        profile = UserProfile.objects.select_related('user').get(user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)


class TicketViewSet(viewsets.ModelViewSet):
    """
    ViewSet completo para tickets.
    
    Endpoints:
    - GET /api/tickets/ - Lista todos los tickets (con filtros)
    - POST /api/tickets/ - Crear nuevo ticket
    - GET /api/tickets/{id}/ - Detalle de un ticket
    - PUT /api/tickets/{id}/ - Actualizar ticket completo
    - PATCH /api/tickets/{id}/ - Actualizar ticket parcial
    - DELETE /api/tickets/{id}/ - Eliminar ticket (solo admin)
    - POST /api/tickets/{id}/close/ - Cerrar ticket
    - POST /api/tickets/{id}/reopen/ - Reabrir ticket
    - GET /api/tickets/my_tickets/ - Tickets creados por el usuario actual
    - GET /api/tickets/assigned_to_me/ - Tickets asignados al usuario actual
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'created_by', 'assigned_to']
    search_fields = ['title', 'description', 'id']
    ordering_fields = ['created_at', 'updated_at', 'priority']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Optimiza las consultas incluyendo relaciones.
        """
        return Ticket.objects.select_related(
            'created_by',
            'assigned_to'
        ).prefetch_related(
            'comments',
            'comments__author'
        ).all()
    
    def get_serializer_class(self):
        """
        Usa diferentes serializadores según la acción.
        """
        if self.action == 'list':
            return TicketSerializer
        elif self.action == 'create':
            return TicketCreateSerializer
        elif self.action in ['close', 'reopen']:
            return TicketStatusUpdateSerializer
        return TicketDetailSerializer
    
    def perform_create(self, serializer):
        """
        Al crear un ticket, asigna automáticamente el usuario actual como creador.
        """
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'], url_path='my-tickets')
    def my_tickets(self, request):
        """
        Retorna los tickets creados por el usuario actual.
        
        GET /api/tickets/my-tickets/
        """
        tickets = self.get_queryset().filter(created_by=request.user)
        
        # Aplicar filtros de búsqueda y ordenamiento
        tickets = self.filter_queryset(tickets)
        
        page = self.paginate_queryset(tickets)
        if page is not None:
            serializer = TicketSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='assigned-to-me')
    def assigned_to_me(self, request):
        """
        Retorna los tickets asignados al usuario actual.
        
        GET /api/tickets/assigned-to-me/
        """
        tickets = self.get_queryset().filter(assigned_to=request.user)
        
        # Aplicar filtros de búsqueda y ordenamiento
        tickets = self.filter_queryset(tickets)
        
        page = self.paginate_queryset(tickets)
        if page is not None:
            serializer = TicketSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        """
        Cierra un ticket.
        
        POST /api/tickets/{id}/close/
        """
        ticket = self.get_object()
        
        if ticket.status == 'cerrado':
            return Response(
                {'error': 'El ticket ya está cerrado.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ticket.status = 'cerrado'
        ticket.save()
        
        serializer = TicketDetailSerializer(ticket)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reopen(self, request, pk=None):
        """
        Reabre un ticket cerrado.
        
        POST /api/tickets/{id}/reopen/
        
        Nota: Solo usuarios staff pueden reabrir tickets.
        """
        ticket = self.get_object()
        
        if not request.user.is_staff:
            return Response(
                {'error': 'No tienes permisos para reabrir tickets cerrados.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if ticket.status != 'cerrado':
            return Response(
                {'error': 'El ticket no está cerrado.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ticket.status = 'abierto'
        ticket.closed_at = None
        ticket.save()
        
        serializer = TicketDetailSerializer(ticket)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet completo para comentarios.
    
    Endpoints:
    - GET /api/comments/ - Lista todos los comentarios
    - POST /api/comments/ - Crear nuevo comentario
    - GET /api/comments/{id}/ - Detalle de un comentario
    - PUT /api/comments/{id}/ - Actualizar comentario completo
    - PATCH /api/comments/{id}/ - Actualizar comentario parcial
    - DELETE /api/comments/{id}/ - Eliminar comentario (solo el autor o admin)
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ticket', 'author', 'is_internal']
    search_fields = ['content']
    ordering_fields = ['created_at']
    ordering = ['created_at']
    
    def get_queryset(self):
        """
        Optimiza las consultas y filtra comentarios internos según permisos.
        """
        queryset = Comment.objects.select_related('ticket', 'author').all()
        
        # Si no es staff, no mostrar comentarios internos de otros
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_internal=False)
        
        return queryset
    
    def perform_create(self, serializer):
        """
        Al crear un comentario, asigna automáticamente el usuario actual como autor.
        """
        serializer.save(author=self.request.user)
    
    def perform_destroy(self, instance):
        """
        Solo el autor del comentario o un admin pueden eliminarlo.
        """
        if instance.author != self.request.user and not self.request.user.is_staff:
            return Response(
                {'error': 'No tienes permisos para eliminar este comentario.'},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()
