"""
URLs de la aplicación tickets.
Configura los endpoints de la API REST.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TicketViewSet,
    CommentViewSet,
    UserProfileViewSet,
    UserViewSet
)

# Crear el router y registrar los ViewSets
router = DefaultRouter()
router.register(r'tickets', TicketViewSet, basename='ticket')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'users', UserViewSet, basename='user')

# Las URLs serán:
# /api/tickets/
# /api/tickets/{id}/
# /api/tickets/my-tickets/
# /api/tickets/assigned-to-me/
# /api/tickets/{id}/close/
# /api/tickets/{id}/reopen/
# /api/comments/
# /api/comments/{id}/
# /api/profiles/
# /api/profiles/{id}/
# /api/profiles/me/
# /api/users/
# /api/users/{id}/

urlpatterns = [
    path('', include(router.urls)),
]
