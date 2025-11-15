from rest_framework.test import APITestCase
from django.urls import reverse
from app.models import Friend
from django.core.files.uploadedfile import SimpleUploadedFile


class FriendAPITest(APITestCase):

    def setUp(self):
        self.friend = Friend.objects.create(
            name="John",
            profession="Developer",
            profession_description="Writes code"
        )
        self.list_url = reverse("friend-list")  # DRF роутер
        self.detail_url = reverse("friend-detail", args=[self.friend.id])

    def test_get_friends_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_get_friend_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "John")

    def test_create_friend_with_photo(self):
        photo = SimpleUploadedFile("photo.jpg", b"content", content_type="image/jpeg")
        data = {
            "name": "Alice",
            "profession": "Tester",
            "profession_description": "Tests code"
        }
        response = self.client.post(self.list_url, data=data, format='multipart', files={"photo_url": photo})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Friend.objects.count(), 2)
