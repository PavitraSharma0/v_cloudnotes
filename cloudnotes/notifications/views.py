from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Notification


@login_required
def notifications_list(request):
    notifications = Notification.objects.filter(
        recipient=request.user
    ).select_related('actor', 'post', 'comment')

    return render(
        request,
        'notifications/notifications.html',
        {
            'notifications': notifications,
        }
    )