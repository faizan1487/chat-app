from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Account
from friend.models import FriendList

@receiver(post_save, sender=Account)
def account_post_save(sender, instance, created, **kwargs):
    if created:
        FriendList.objects.create(user=instance)
        