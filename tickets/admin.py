"""
Configuración del panel de administración de Django para el sistema de tickets.
Personaliza cómo se muestran los modelos en /admin/
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Ticket, Comment, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Configuración del admin para UserProfile."""
    
    list_display = [
        'user',
        'department',
        'phone',
        'is_support_staff',
        'created_at'
    ]
    
    list_filter = [
        'is_support_staff',
        'department',
        'created_at'
    ]
    
    search_fields = [
        'user__username',
        'user__email',
        'user__first_name',
        'user__last_name',
        'department',
        'phone'
    ]
    
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información del Usuario', {
            'fields': ('user',)
        }),
        ('Información Laboral', {
            'fields': ('department', 'phone', 'is_support_staff')
        }),
        ('Avatar', {
            'fields': ('avatar',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class CommentInline(admin.TabularInline):
    """
    Inline para mostrar comentarios dentro del ticket.
    Permite ver y editar comentarios directamente desde la página del ticket.
    """
    model = Comment
    extra = 0  # No mostrar formularios vacíos por defecto
    fields = ['author', 'content', 'is_internal', 'attachment', 'created_at']
    readonly_fields = ['created_at']
    
    def has_delete_permission(self, request, obj=None):
        """Solo staff puede eliminar comentarios."""
        return request.user.is_staff


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """Configuración del admin para Ticket."""
    
    list_display = [
        'id',
        'title',
        'status_badge',
        'priority_badge',
        'created_by',
        'assigned_to',
        'days_open',
        'created_at'
    ]
    
    list_filter = [
        'status',
        'priority',
        'created_at',
        'updated_at',
        ('assigned_to', admin.EmptyFieldListFilter),
    ]
    
    search_fields = [
        'title',
        'description',
        'id',
        'created_by__username',
        'created_by__email',
        'assigned_to__username',
        'assigned_to__email'
    ]
    
    readonly_fields = [
        'created_at',
        'updated_at',
        'closed_at',
        'days_open',
        'is_open',
        'is_closed'
    ]
    
    # Mostrar comentarios dentro del ticket
    inlines = [CommentInline]
    
    # Organizar campos en secciones
    fieldsets = (
        ('Información Básica', {
            'fields': ('title', 'description')
        }),
        ('Estado y Prioridad', {
            'fields': ('status', 'priority')
        }),
        ('Asignación', {
            'fields': ('created_by', 'assigned_to')
        }),
        ('Fechas e Información Adicional', {
            'fields': (
                'created_at',
                'updated_at',
                'closed_at',
                'days_open',
                'is_open',
                'is_closed'
            ),
            'classes': ('collapse',)
        }),
    )
    
    # Orden por defecto (más recientes primero)
    ordering = ['-created_at']
    
    # Número de items por página
    list_per_page = 25
    
    # Métodos personalizados para badges de colores
    @admin.display(description='Estado')
    def status_badge(self, obj):
        """Muestra el estado con un badge de color."""
        colors = {
            'abierto': 'green',
            'en_progreso': 'blue',
            'cerrado': 'gray'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    
    @admin.display(description='Prioridad')
    def priority_badge(self, obj):
        """Muestra la prioridad con un badge de color."""
        colors = {
            'alta': '#dc3545',
            'media': '#ffc107',
            'baja': '#28a745'
        }
        color = colors.get(obj.priority, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_priority_display()
        )
    
    def save_model(self, request, obj, form, change):
        """
        Al guardar, si no tiene creador, asignar el usuario actual.
        """
        if not change:  # Si es un nuevo ticket
            if not obj.created_by:
                obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Configuración del admin para Comment."""
    
    list_display = [
        'id',
        'ticket',
        'author',
        'content_preview',
        'is_internal',
        'has_attachment',
        'created_at'
    ]
    
    list_filter = [
        'is_internal',
        'created_at',
        'updated_at'
    ]
    
    search_fields = [
        'content',
        'ticket__title',
        'author__username',
        'author__email'
    ]
    
    readonly_fields = ['created_at', 'updated_at', 'is_edited']
    
    fieldsets = (
        ('Información del Comentario', {
            'fields': ('ticket', 'author', 'content')
        }),
        ('Adjuntos y Opciones', {
            'fields': ('attachment', 'is_internal')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at', 'is_edited'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-created_at']
    list_per_page = 50
    
    @admin.display(description='Contenido')
    def content_preview(self, obj):
        """Muestra una vista previa del contenido del comentario."""
        max_length = 50
        if len(obj.content) > max_length:
            return f"{obj.content[:max_length]}..."
        return obj.content
    
    @admin.display(description='Adjunto', boolean=True)
    def has_attachment(self, obj):
        """Indica si el comentario tiene un archivo adjunto."""
        return bool(obj.attachment)
    
    def save_model(self, request, obj, form, change):
        """
        Al guardar, si no tiene autor, asignar el usuario actual.
        """
        if not change:  # Si es un nuevo comentario
            if not obj.author:
                obj.author = request.user
        super().save_model(request, obj, form, change)
