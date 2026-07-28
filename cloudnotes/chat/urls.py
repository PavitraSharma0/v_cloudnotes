from django.urls import path
from . import views

urlpatterns = [
    # Inbox – list of all conversations
    path('', views.inbox, name='chat_inbox'),

    # Start a new chat (user list)
    path('new/', views.new_chat, name='chat_new'),

    # Conversation detail by ID
    path('<int:convo_id>/', views.conversation_detail, name='chat_conversation'),

    # Create / redirect to conversation using username
    path('<str:username>/', views.chat_room, name='chat_room'),
]