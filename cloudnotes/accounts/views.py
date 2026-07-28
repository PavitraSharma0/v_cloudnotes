from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone

from .forms import SignupForm
from .utils import send_html_email

from posts.models import Post
from social.models import Follow


# -------------------------
# LOGIN
# -------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # Send login alert email
            send_html_email(
                subject="New Login to Your CloudNotes Account",
                template="accounts/email_login_response.html",
                context={
                    "user": user,
                    "login_time": timezone.now().strftime("%d %b %Y, %I:%M %p"),
                    "ip_address": request.META.get("REMOTE_ADDR"),
                    "user_agent": request.META.get(
                        "HTTP_USER_AGENT", "Unknown device"
                    ),
                    "year": timezone.now().year,
                },
                to_email=user.email,
            )

            return redirect("dashboard")

        messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")


# -------------------------
# SIGNUP
# -------------------------
def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()

            # Send welcome email
            send_html_email(
                subject="Welcome to CloudNotes 🎉",
                template="accounts/email_signup_response.html",
                context={
                    "user": user,
                    "login_url": request.build_absolute_uri("/accounts/login/"),
                    "year": timezone.now().year,
                },
                to_email=user.email,
            )

            messages.success(
                request, "Account created successfully. Please log in."
            )
            return redirect("login")
    else:
        form = SignupForm()

    return render(request, "accounts/signup.html", {"form": form})


# -------------------------
# LOGOUT
# -------------------------
@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


# -------------------------
# PROFILE
# -------------------------
@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)

    posts = Post.objects.filter(
        author=profile_user, status="published"
    ).order_by("-created_at")

    context = {
        "profile_user": profile_user,
        "posts": posts,
        "posts_count": posts.count(),
        "followers_count": Follow.objects.filter(
            following=profile_user
        ).count(),
        "following_count": Follow.objects.filter(
            follower=profile_user
        ).count(),
        "is_following": Follow.objects.filter(
            follower=request.user,
            following=profile_user
        ).exists() if request.user.is_authenticated else False,
    }

    return render(request, "accounts/profile.html", context)