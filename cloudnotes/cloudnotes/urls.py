from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('dashboard.urls')),

    path('accounts/', include('accounts.urls')),
    path('posts/', include('posts.urls')),
    path('social/', include('social.urls')),
    path('chat/', include('chat.urls')),
    path('notifications/', include('notifications.urls')),
    path('ai/', include('ai.urls')),
    path("search/", include("search.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)