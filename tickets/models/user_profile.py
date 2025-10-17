"""
Modelo UserProfile - Perfil extendido de usuario.
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    Perfil extendido de usuario para el sistema de tickets.
    
    Almacena información adicional de los usuarios más allá
    del modelo User predeterminado de Django.
    """
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Usuario',
        primary_key=True
    )
    
    department = models.CharField(
        max_length=100,
        verbose_name='Departamento',
        help_text='Departamento al que pertenece el usuario',
        blank=True
    )
    
    phone = models.CharField(
        max_length=20,
        verbose_name='Teléfono',
        help_text='Número de teléfono de contacto',
        blank=True
    )
    
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        verbose_name='Avatar',
        help_text='Imagen de perfil del usuario (máximo 5MB)'
    )
    
    is_support_staff = models.BooleanField(
        default=False,
        verbose_name='Personal de soporte',
        help_text='Indica si el usuario pertenece al equipo de soporte'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de registro'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Última actualización'
    )
    
    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuario'
        ordering = ['-created_at']
    
    def __str__(self):
        full_name = self.user.get_full_name()
        return f"Perfil de {full_name if full_name else self.user.username}"


# Signal para crear automáticamente el perfil cuando se crea un usuario
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal que crea automáticamente un UserProfile
    cuando se crea un nuevo usuario.
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal que guarda el perfil del usuario
    cuando se guarda el usuario.
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()
