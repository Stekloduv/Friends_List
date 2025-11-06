from django.test import TestCase
from app.models import Friend
from django.core.files.uploadedfile import SimpleUploadedFile

class FriendModelTest(TestCase):

    def test_create_friend(self):
        photo = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        friend = Friend.objects.create(
            name="John Doe",
            profession="Developer",
            profession_description="Writes code",
            photo_url=photo
        )
        self.assertEqual(friend.name, "John Doe")
        self.assertEqual(friend.profession, "Developer")
        self.assertTrue(friend.photo_url.name.endswith("test.jpg"))

    def test_friend_str(self):
        friend = Friend.objects.create(name="Alice", profession="Tester")
        self.assertEqual(str(friend), "Alice")
