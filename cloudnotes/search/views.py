from django.shortcuts import render
from django.contrib.auth.models import User
from posts.models import Post

def search_view(request):
    query = request.GET.get("q", "").strip()

    users = []
    posts = []

    if query:
        users = User.objects.filter(username__icontains=query)
        posts = Post.objects.filter(
            title__icontains=query,
            status="published"
        )

    context = {
        "query": query,
        "users": users,
        "posts": posts,
    }

    return render(request, "search/results.html", context)