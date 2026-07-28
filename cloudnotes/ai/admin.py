from django.contrib import admin
from .models import AIMessage


@admin.register(AIMessage)
class AIMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'sender', 'created_at')
    list_filter = ('sender', 'created_at')
    search_fields = ('content', 'user__username')