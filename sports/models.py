from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        return self.name

class Message(models.Model):
    room = models.ForeignKey(Room,related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name='messages', on_delete=models.CASCADE,default=None)
    content = models.TextField(default='')
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)
