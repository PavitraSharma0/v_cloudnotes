from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class AIMessage(models.Model):
    SENDER_CHOICES = (
        ('user', 'User'),
        ('ai', 'AI'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ai_messages'
    )
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user} - {self.sender}"