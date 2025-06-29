from django.contrib.auth import get_user_model

from senjor import models


# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name="sender")  # type: ignore
    receiver = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name="receiver")  # type: ignore
    content = models.TextField()


class ChatRoom(models.Model):
    name = models.CharField(max_length=100)
    messages = models.ManyToManyField(Message)
