from django.urls import path
from . import views

urlpatterns = [
    path("followers/<str:username>/", views.followers_view, name="followers"),
    path("following/<str:username>/", views.following_view, name="following"),
    path("follow/<str:username>/", views.toggle_follow, name="toggle_follow"),
]