from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from posts.models import Post
from .models import Follow


def followers_view(request, username):
    profile_user = get_object_or_404(User, username=username)

    followers_qs = User.objects.filter(
        following_relations__following=profile_user
    ).select_related("profile")

    following_ids = []
    if request.user.is_authenticated:
        following_ids = list(
            Follow.objects.filter(follower=request.user)
            .values_list("following_id", flat=True)
        )

    context = {
        "profile_user": profile_user,
        "followers": followers_qs,
        "followers_count": followers_qs.count(),
        "following_count": Follow.objects.filter(follower=profile_user).count(),
        "posts_count": Post.objects.filter(author=profile_user).count(),
        "following_ids": following_ids,
    }

    return render(request, "social/followers.html", context)


def following_view(request, username):
    profile_user = get_object_or_404(User, username=username)

    following_qs = User.objects.filter(
        follower_relations__follower=profile_user
    ).select_related("profile")

    following_ids = []
    if request.user.is_authenticated:
        following_ids = list(
            Follow.objects.filter(follower=request.user)
            .values_list("following_id", flat=True)
        )

    context = {
        "profile_user": profile_user,
        "following": following_qs,
        "following_count": following_qs.count(),
        "followers_count": Follow.objects.filter(following=profile_user).count(),
        "posts_count": Post.objects.filter(author=profile_user).count(),
        "following_ids": following_ids,
    }

    return render(request, "social/following.html", context)

@login_required
def toggle_follow(request, username):
    target_user = get_object_or_404(User, username=username)

    if target_user == request.user:
        return redirect('profile', username=username)

    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=target_user
    )

    if not created:
        follow.delete()

    return redirect('profile', username=username)