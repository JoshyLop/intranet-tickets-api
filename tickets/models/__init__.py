"""
Modelos para la aplicación de tickets.

Este paquete contiene todos los modelos de datos:
- Ticket: Modelo principal de tickets
- Comment: Comentarios en tickets
- UserProfile: Perfiles extendidos de usuario
"""

from .ticket import Ticket
from .comment import Comment
from .user_profile import UserProfile

__all__ = ['Ticket', 'Comment', 'UserProfile']
