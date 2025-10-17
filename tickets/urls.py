"""
URLs for the tickets app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Placeholder - will be populated with ViewSets later
router = DefaultRouter()

# Placeholder routes (to be implemented)
# router.register(r'tickets', TicketViewSet, basename='ticket')
# router.register(r'comments', CommentViewSet, basename='comment')
# router.register(r'profiles', UserProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
]
