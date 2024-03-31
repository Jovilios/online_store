from django.db import models
from django.utils import timezone
from online_store.accounts.models import CustomUser
from online_store.products.models import Product


class Message(models.Model):
    sender = models.ForeignKey(CustomUser, related_name="sent_messages", on_delete=models.CASCADE)
    recipient = models.ForeignKey(CustomUser, related_name="received_messages", on_delete=models.CASCADE)
    subject = models.CharField(max_length=200, blank=True, null=True)
    body = models.TextField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.subject
