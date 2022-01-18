from django.db import models
from django.conf import settings
import random

User = settings.AUTH_USER_MODEL

class SpeakLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    speak = models.ForeignKey("Speak", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Speak(models.Model):
    # id = models.AutoField(primary_key=True)   is behind the scenes
     # blank=True means not required in Django, null=True not required in database
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='speak_user', blank=True, through=SpeakLike)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)



    # shows the content of each post in the admin (instead of "object 57" for example)
    def __str__(self):
        return self.content


    class Meta:
        ordering = ['-id'] # reverses the order of the id's

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 500),
        }
   