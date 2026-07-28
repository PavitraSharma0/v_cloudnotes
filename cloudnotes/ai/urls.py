from django.urls import path
from . import views

urlpatterns = [
    path('', views.assistant, name='ai_assistant'),
    path('ask/', views.ai_ask, name='ai_ask'),
]