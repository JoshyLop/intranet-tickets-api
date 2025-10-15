from django.db import models
from django.contrib.auth.models import User


class Ticket(models.Model):
    """
    Modelo para gestionar tickets de la intranet.
    """
    
    # Choices para estado
    ESTADO_CHOICES = [
        ('abierto', 'Abierto'),
        ('en_progreso', 'En Progreso'),
        ('resuelto', 'Resuelto'),
        ('cerrado', 'Cerrado'),
    ]
    
    # Choices para prioridad
    PRIORIDAD_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('critica', 'Crítica'),
    ]
    
    titulo = models.CharField(
        max_length=200,
        verbose_name='Título',
        help_text='Título breve del ticket'
    )
    descripcion = models.TextField(
        verbose_name='Descripción',
        help_text='Descripción detallada del problema o solicitud'
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='abierto',
        verbose_name='Estado',
        help_text='Estado actual del ticket'
    )
    prioridad = models.CharField(
        max_length=20,
        choices=PRIORIDAD_CHOICES,
        default='media',
        verbose_name='Prioridad',
        help_text='Prioridad del ticket'
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tickets',
        verbose_name='Usuario',
        help_text='Usuario que creó el ticket'
    )
    creado_en = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    actualizado_en = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Actualización'
    )
    
    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'
        ordering = ['-creado_en']
    
    def __str__(self):
        return f"{self.titulo} - {self.get_estado_display()}"
