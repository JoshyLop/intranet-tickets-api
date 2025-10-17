"""
Modelo Ticket - Gestión de tickets de soporte.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator


class Ticket(models.Model):
    """
    Modelo principal para gestionar tickets en el sistema.
    
    Representa una solicitud o incidente reportado por un usuario
    que debe ser atendido por el equipo de soporte.
    """
    
    # Opciones de Estado
    STATUS_CHOICES = [
        ('abierto', 'Abierto'),
        ('en_progreso', 'En Progreso'),
        ('cerrado', 'Cerrado'),
    ]
    
    # Opciones de Prioridad
    PRIORITY_CHOICES = [
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
    ]
    
    # Campos principales
    title = models.CharField(
        max_length=200,
        verbose_name='Título',
        help_text='Título descriptivo del ticket',
        validators=[MinLengthValidator(5, 'El título debe tener al menos 5 caracteres')]
    )
    
    description = models.TextField(
        verbose_name='Descripción',
        help_text='Descripción detallada del problema o solicitud',
        validators=[MinLengthValidator(10, 'La descripción debe tener al menos 10 caracteres')]
    )
    
    # Estado y Prioridad
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='abierto',
        verbose_name='Estado',
        db_index=True
    )
    
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='media',
        verbose_name='Prioridad',
        db_index=True
    )
    
    # Relaciones con Usuario
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tickets_created',
        verbose_name='Creado por',
        db_index=True
    )
    
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tickets_assigned',
        verbose_name='Asignado a'
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación',
        db_index=True
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Última actualización'
    )
    
    closed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de cierre'
    )
    
    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'
        ordering = ['-created_at', '-priority']
        indexes = [
            models.Index(fields=['-created_at', 'status']),
            models.Index(fields=['priority', 'status']),
        ]
    
    def __str__(self):
        return f"#{self.id} - {self.title} [{self.get_status_display()}]"
    
    def save(self, *args, **kwargs):
        """
        Override para actualizar automáticamente la fecha de cierre
        cuando el ticket cambia a estado 'cerrado'.
        """
        from django.utils import timezone
        
        if self.status == 'cerrado' and not self.closed_at:
            self.closed_at = timezone.now()
        elif self.status != 'cerrado' and self.closed_at:
            self.closed_at = None
        
        super().save(*args, **kwargs)
    
    @property
    def is_open(self):
        """Retorna True si el ticket está abierto o en progreso."""
        return self.status in ['abierto', 'en_progreso']
    
    @property
    def is_closed(self):
        """Retorna True si el ticket está cerrado."""
        return self.status == 'cerrado'
    
    @property
    def days_open(self):
        """Calcula los días que el ticket ha estado abierto."""
        from django.utils import timezone
        
        end_date = self.closed_at if self.closed_at else timezone.now()
        return (end_date - self.created_at).days
