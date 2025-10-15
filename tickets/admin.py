from django.contrib import admin
from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para Tickets.
    """
    list_display = ['id', 'titulo', 'estado', 'prioridad', 'usuario', 'creado_en', 'actualizado_en']
    list_filter = ['estado', 'prioridad', 'creado_en', 'actualizado_en']
    search_fields = ['titulo', 'descripcion', 'usuario__username', 'usuario__email']
    readonly_fields = ['creado_en', 'actualizado_en']
    list_per_page = 25
    
    fieldsets = (
        ('Información del Ticket', {
            'fields': ('titulo', 'descripcion')
        }),
        ('Estado y Prioridad', {
            'fields': ('estado', 'prioridad')
        }),
        ('Asignación', {
            'fields': ('usuario',)
        }),
        ('Fechas', {
            'fields': ('creado_en', 'actualizado_en'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """
        Al crear un nuevo ticket desde el admin, asigna el usuario actual si no se especificó.
        """
        if not change and not obj.usuario_id:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)
