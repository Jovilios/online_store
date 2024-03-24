from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from online_store.accounts.models import UserProfile


@receiver(post_save, sender=get_user_model())
def create_and_save_user_profile(sender, instance, created, **kwargs) -> None:
    if created:
        UserProfile.objects.get_or_create(user=instance)
