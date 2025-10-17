"""
Modelo Comment - Comentarios en tickets.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator


class Comment(models.Model):
    """
    Modelo para comentarios en tickets.
    
    Permite a los usuarios y al personal de soporte comunicarse
    dentro del contexto de un ticket específico.
    """
    
    ticket = models.ForeignKey(
        'Ticket',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Ticket',
        help_text='Ticket al que pertenece este comentario'
    )
    
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Autor',
        help_text='Usuario que escribió el comentario'
    )
    
    content = models.TextField(
        verbose_name='Contenido',
        help_text='Texto del comentario',
        validators=[MinLengthValidator(3, 'El comentario debe tener al menos 3 caracteres')]
    )
    
    attachment = models.FileField(
        upload_to='attachments/%Y/%m/%d/',
        null=True,
        blank=True,
        verbose_name='Adjunto',
        help_text='Archivo adjunto opcional (máximo 10MB)'
    )
    
    is_internal = models.BooleanField(
        default=False,
        verbose_name='Comentario interno',
        help_text='Si es True, solo visible para el personal de soporte'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Última edición'
    )
    
    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['ticket', 'created_at']),
            models.Index(fields=['author']),
        ]
    
    def __str__(self):
        return f"Comentario de {self.author.username} en Ticket #{self.ticket.id}"
    
    @property
    def is_edited(self):
        """Retorna True si el comentario fue editado después de su creación."""
        return self.updated_at > self.created_at
