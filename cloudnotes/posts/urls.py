from django.urls import path
from . import views

urlpatterns = [
    # ---------------------------
    # Browse / Discover
    # ---------------------------
    path(
        "",
        views.browse,
        name="browse",
    ),

    # ---------------------------
    # Upload & Manage Posts
    # ---------------------------
    path(
        "upload/",
        views.upload_post,
        name="upload_post",
    ),
    path(
        "my-uploads/",
        views.my_uploads,
        name="my_uploads",
    ),

    # ---------------------------
    # Post Detail
    # ---------------------------
    path(
        "post/<str:post_id>/",
        views.post_detail,
        name="post_detail",
    ),

    # ---------------------------
    # Saved Posts Page
    # ---------------------------
    path(
        "saved/",
        views.saved_posts,
        name="saved_posts",
    ),

    # ---------------------------
    # Actions (Like / Save)
    # ---------------------------
    path(
        "like/<str:post_id>/",
        views.toggle_like,
        name="toggle_like",
    ),
    path(
        "save/<str:post_id>/",
        views.toggle_save,
        name="toggle_save",
    ),
]