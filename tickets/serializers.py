from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Ticket, Comment, UserProfile


class UserSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo User de Django.
    
    Incluye información básica del usuario y campos de solo lectura.
    """
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'is_active',
            'date_joined',
        ]
        read_only_fields = ['id', 'date_joined']
    
    def get_full_name(self, obj):
        """Retorna el nombre completo del usuario."""
        return obj.get_full_name() or obj.username


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo UserProfile.
    
    Incluye información del usuario relacionado de forma anidada.
    """
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = UserProfile
        fields = [
            'user',
            'user_id',
            'department',
            'phone',
            'avatar',
            'is_support_staff',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_avatar(self, value):
        """Valida el tamaño y tipo del avatar."""
        if value:
            # Validar tamaño (máximo 5MB)
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError(
                    "El tamaño del avatar no puede exceder 5MB."
                )
            
            # Validar tipo de archivo
            allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
            if value.content_type not in allowed_types:
                raise serializers.ValidationError(
                    "El avatar debe ser una imagen en formato JPG, PNG, GIF o WebP."
                )
        
        return value


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Comment.
    
    Incluye información del autor y permite crear comentarios con archivos adjuntos.
    """
    author = UserSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True, required=False)
    author_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            'id',
            'ticket',
            'author',
            'author_id',
            'author_name',
            'content',
            'attachment',
            'is_internal',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_author_name(self, obj):
        """Retorna el nombre del autor del comentario."""
        return obj.author.get_full_name() or obj.author.username
    
    def validate_content(self, value):
        """Valida que el contenido del comentario no esté vacío."""
        if not value or len(value.strip()) < 3:
            raise serializers.ValidationError(
                "El comentario debe tener al menos 3 caracteres."
            )
        return value.strip()
    
    def validate_attachment(self, value):
        """Valida el tamaño del archivo adjunto."""
        if value:
            # Validar tamaño (máximo 10MB)
            if value.size > 10 * 1024 * 1024:
                raise serializers.ValidationError(
                    "El archivo adjunto no puede exceder 10MB."
                )
        return value
    
    def create(self, validated_data):
        """Crea un nuevo comentario asignando automáticamente el autor."""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['author'] = request.user
        return super().create(validated_data)


class TicketSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Ticket.
    
    Incluye información detallada del ticket, usuarios relacionados y comentarios.
    """
    created_by = UserSerializer(read_only=True)
    created_by_id = serializers.IntegerField(write_only=True, required=False)
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    # Campos adicionales calculados
    comments_count = serializers.SerializerMethodField()
    is_open = serializers.BooleanField(read_only=True)
    is_closed = serializers.BooleanField(read_only=True)
    days_open = serializers.IntegerField(read_only=True)
    
    # Campos de texto para mostrar las opciones legibles
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    
    class Meta:
        model = Ticket
        fields = [
            'id',
            'title',
            'description',
            'status',
            'status_display',
            'priority',
            'priority_display',
            'created_by',
            'created_by_id',
            'assigned_to',
            'assigned_to_id',
            'created_at',
            'updated_at',
            'closed_at',
            'comments_count',
            'is_open',
            'is_closed',
            'days_open',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'closed_at']
    
    def get_comments_count(self, obj):
        """Retorna el número de comentarios del ticket."""
        return obj.comments.count()
    
    def validate_title(self, value):
        """Valida que el título tenga una longitud mínima."""
        if not value or len(value.strip()) < 5:
            raise serializers.ValidationError(
                "El título debe tener al menos 5 caracteres."
            )
        return value.strip()
    
    def validate_description(self, value):
        """Valida que la descripción tenga una longitud mínima."""
        if not value or len(value.strip()) < 10:
            raise serializers.ValidationError(
                "La descripción debe tener al menos 10 caracteres."
            )
        return value.strip()
    
    def validate_status(self, value):
        """Valida las transiciones de estado del ticket."""
        if self.instance:
            # Validar transiciones de estado
            old_status = self.instance.status
            
            # No permitir reabrir tickets cerrados sin permisos especiales
            if old_status == 'cerrado' and value != 'cerrado':
                request = self.context.get('request')
                if request and not request.user.is_staff:
                    raise serializers.ValidationError(
                        "No tienes permisos para reabrir un ticket cerrado."
                    )
        
        return value
    
    def create(self, validated_data):
        """Crea un nuevo ticket asignando automáticamente el creador."""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        return super().create(validated_data)


class TicketDetailSerializer(TicketSerializer):
    """
    Serializador detallado para el modelo Ticket.
    
    Incluye la lista completa de comentarios anidados.
    Se usa para las vistas de detalle individual.
    """
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta(TicketSerializer.Meta):
        fields = TicketSerializer.Meta.fields + ['comments']


class TicketCreateSerializer(serializers.ModelSerializer):
    """
    Serializador simplificado para la creación de tickets.
    
    Solo incluye los campos necesarios para crear un nuevo ticket.
    """
    
    class Meta:
        model = Ticket
        fields = [
            'title',
            'description',
            'priority',
            'assigned_to',
        ]
    
    def validate_title(self, value):
        """Valida que el título tenga una longitud mínima."""
        if not value or len(value.strip()) < 5:
            raise serializers.ValidationError(
                "El título debe tener al menos 5 caracteres."
            )
        return value.strip()
    
    def validate_description(self, value):
        """Valida que la descripción tenga una longitud mínima."""
        if not value or len(value.strip()) < 10:
            raise serializers.ValidationError(
                "La descripción debe tener al menos 10 caracteres."
            )
        return value.strip()
    
    def create(self, validated_data):
        """Crea un nuevo ticket asignando el creador y estado inicial."""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        validated_data['status'] = 'abierto'
        return super().create(validated_data)


class TicketStatusUpdateSerializer(serializers.ModelSerializer):
    """
    Serializador para actualizar solo el estado de un ticket.
    
    Útil para endpoints específicos de cambio de estado.
    """
    
    class Meta:
        model = Ticket
        fields = ['status']
    
    def validate_status(self, value):
        """Valida las transiciones de estado."""
        if self.instance:
            old_status = self.instance.status
            
            # Validar que no se reabran tickets cerrados sin permisos
            if old_status == 'cerrado' and value != 'cerrado':
                request = self.context.get('request')
                if request and not request.user.is_staff:
                    raise serializers.ValidationError(
                        "No tienes permisos para reabrir un ticket cerrado."
                    )
        
        return value
