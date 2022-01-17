from django.db import models
import random

class Speak(models.Model):
    # id = models.AutoField(primary_key=True)   is behind the scenes
     # blank=True means not required in Django, null=True not required in database
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)

    class Meta:
        ordering = ['-id'] # reverses the order of the id's

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 500),
        }
   