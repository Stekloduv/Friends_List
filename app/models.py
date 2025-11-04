import uuid

from django.db import models

class Friend(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    neme = models.TextField(blank=False, null=False)
    profession = models.TextField(blank=False, null=False)
    profession_description = models.TextField(blank=True, null=True)
    photo_url = models.URLField(blank=False, null=False)


