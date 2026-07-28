from django.db.models.signals import post_save
from django.dispatch import receiver

from posts.models import Comment
from social.models import Follow
from .models import Notification


# 🔔 Comment Notification
@receiver(post_save, sender=Comment)
def notify_comment(sender, instance, created, **kwargs):
    """
    Notify post author when someone comments on their post
    """
    if created and instance.post.author != instance.author:
        Notification.objects.create(
            recipient=instance.post.author,
            actor=instance.author,
            type='comment',
            post=instance.post,
            comment=instance
        )


# 🔔 Follow Notification
@receiver(post_save, sender=Follow)
def notify_follow(sender, instance, created, **kwargs):
    """
    Notify user when someone follows them
    """
    if created:
        Notification.objects.create(
            recipient=instance.following,   # ✅ FIXED
            actor=instance.follower,        # ✅ CORRECT
            type='follow'
        )