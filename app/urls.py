from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FriendViewSet

router = DefaultRouter()
router.register(r'friends', FriendViewSet, basename='friend')

urlpatterns = [
    path('', include(router.urls)),
]
