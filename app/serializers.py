from rest_framework import serializers
from .models import Friend


class FriendSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Friend
        fields = ['id', 'name', 'profession', 'profession_description', 'photo_url']

    def get_photo_url(self, obj):
        request = self.context.get('request')
        if obj.photo:
            return request.build_absolute_uri(obj.photo_url.url)
        return None