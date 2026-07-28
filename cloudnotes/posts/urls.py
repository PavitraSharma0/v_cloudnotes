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
        "post/<int:post_id>/",
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
        "like/<int:post_id>/",
        views.toggle_like,
        name="toggle_like",
    ),
    path(
        "save/<int:post_id>/",
        views.toggle_save,
        name="toggle_save",
    ),
]