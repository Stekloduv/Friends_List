from rest_framework import viewsets
from .models import Friend
from .serializers import FriendsSerializer

class FriendViewSet(viewsets.ModelViewSet):
    queryset = Friend.objects.all()
    serializer_class = FriendsSerializer
