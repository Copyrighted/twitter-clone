from django.db import models
import random
from django.conf import settings
# Create your models here.

User = settings.AUTH_USER_MODEL #use djangos default user settings

class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # so many users can have many tweets, CASCADE will delete all tweets associated with user ID
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)

    class Meta:
        ordering = ['-id']

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 200)
        }