from rest_framework import viewsets, parsers
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Friend
from .serializers import FriendSerializer

class FriendViewSet(viewsets.ModelViewSet):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer
    parser_classes = [MultiPartParser, FormParser]