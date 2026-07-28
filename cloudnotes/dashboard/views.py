from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from posts.models import Post
from notifications.models import Notification
from social.models import Follow


@login_required
def dashboard_home(request):
    user = request.user

    # ---------------------------
    # Saved posts
    # ---------------------------
    saved_posts_qs = Post.objects.filter(saves=user).order_by("-created_at")
    recent_saved_posts = saved_posts_qs[:4]

    # ---------------------------
    # User uploads
    # ---------------------------
    uploads_qs = Post.objects.filter(author=user).order_by("-created_at")
    recent_uploads = uploads_qs[:5]

    # ---------------------------
    # Followers / Following (FIXED)
    # ---------------------------
    followers_count = Follow.objects.filter(following=user).count()
    following_count = Follow.objects.filter(follower=user).count()

    # ---------------------------
    # Notifications
    # ---------------------------
    recent_notifications = (
        Notification.objects
        .filter(recipient=user)
        .select_related("actor")
        .order_by("-created_at")[:5]
    )

    context = {
        # Counters
        "saved_count": saved_posts_qs.count(),
        "uploads_count": uploads_qs.count(),
        "followers_count": followers_count,
        "following_count": following_count,

        # Lists
        "recent_saved_posts": recent_saved_posts,
        "recent_uploads": recent_uploads,
        "recent_notifications": recent_notifications,
    }

    return render(request, "index.html", context)