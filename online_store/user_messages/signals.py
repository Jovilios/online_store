from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from .models import Message


@receiver(post_save, sender=Message)
def send_message_notification(sender, instance, created, **kwargs):
    if created:
        messages.info(instance.recipient, 'You have received a new message.')