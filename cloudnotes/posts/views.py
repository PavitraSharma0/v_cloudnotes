from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Post, Tag, Comment
from .forms import PostCreateForm
from social.models import Follow


# ---------------------------
# Browse / Discover Posts
# ---------------------------
def browse(request):
    query = request.GET.get("q")
    category = request.GET.get("category")
    tag = request.GET.get("tag")

    posts = (
        Post.objects
        .filter(status="published")
        .select_related("author")
        .prefetch_related("tags", "likes", "comments")
        .order_by("-created_at")
    )

    if query:
        posts = posts.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(author__username__icontains=query)
        )

    if category:
        posts = posts.filter(category=category)

    if tag:
        posts = posts.filter(tags__name__iexact=tag)

    context = {
        "posts": posts,
        "categories": Post.CATEGORY_CHOICES,
    }
    return render(request, "posts/browse.html", context)


# ---------------------------
# Post Detail + Comments
# ---------------------------
def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects
        .select_related("author")
        .prefetch_related("tags", "likes", "saves", "comments__author"),
        id=post_id,
        status="published",
    )

    # Safely increment views (atomic)
    Post.objects.filter(id=post.id).update(
        views_count=F("views_count") + 1
    )
    post.refresh_from_db(fields=["views_count"])

    comments = post.comments.all().order_by("-created_at")

    user_liked = False
    user_saved = False
    user_following = False

    if request.user.is_authenticated:
        user_liked = post.likes.filter(id=request.user.id).exists()
        user_saved = post.saves.filter(id=request.user.id).exists()

        user_following = Follow.objects.filter(
            follower=request.user,
            following=post.author
        ).exists()

        # Comment submit
        if request.method == "POST" and "content" in request.POST:
            content = request.POST.get("content", "").strip()
            if content:
                Comment.objects.create(
                    post=post,
                    author=request.user,
                    content=content
                )
                return redirect("post_detail", post_id=post.id)

    related_posts = (
        Post.objects
        .filter(category=post.category, status="published")
        .exclude(id=post.id)
        .select_related("author")[:4]
    )

    context = {
        "post": post,
        "comments": comments,
        "related_posts": related_posts,
        "user_liked": user_liked,
        "user_saved": user_saved,
        "user_following": user_following,
    }
    return render(request, "posts/post_detail.html", context)


# ---------------------------
# Upload Post
# ---------------------------
@login_required
def upload_post(request):
    if request.method == "POST":
        form = PostCreateForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(
                commit=False,
                author=request.user,
                status="published"
                if request.POST.get("action") == "publish"
                else "draft",
            )
            post.save()
            form.save_m2m()
            return redirect("my_uploads")
    else:
        form = PostCreateForm()

    return render(request, "posts/upload.html", {"form": form})


# ---------------------------
# My Uploads
# ---------------------------
@login_required
def my_uploads(request):
    posts = (
        Post.objects
        .filter(author=request.user)
        .prefetch_related("likes", "comments", "saves")
        .order_by("-created_at")
    )

    context = {
        "posts": posts,
        "total_posts": posts.count(),
        "total_likes": sum(p.likes.count() for p in posts),
        "total_comments": sum(p.comments.count() for p in posts),
        "total_views": sum(p.views_count for p in posts),
    }
    return render(request, "posts/my_uploads.html", context)


# ---------------------------
# Saved Posts
# ---------------------------
@login_required
def saved_posts(request):
    posts = (
        Post.objects
        .filter(saves=request.user)
        .select_related("author")
        .prefetch_related("tags")
        .order_by("-created_at")
    )

    categories = posts.values_list("category", flat=True).distinct()

    this_month_count = posts.filter(
        created_at__month=timezone.now().month,
        created_at__year=timezone.now().year,
    ).count()

    context = {
        "saved_posts": posts,
        "categories_count": categories.count(),
        "this_month_count": this_month_count,
    }
    return render(request, "posts/saved.html", context)


# ---------------------------
# Like Post
# ---------------------------
@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(
        request.META.get(
            "HTTP_REFERER",
            reverse("post_detail", args=[post.id]),
        )
    )


# ---------------------------
# Save Post
# ---------------------------
@login_required
def toggle_save(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.saves.filter(id=request.user.id).exists():
        post.saves.remove(request.user)
    else:
        post.saves.add(request.user)

    return HttpResponseRedirect(
        request.META.get(
            "HTTP_REFERER",
            reverse("post_detail", args=[post.id]),
        )
    )