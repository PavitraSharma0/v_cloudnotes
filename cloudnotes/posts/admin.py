from django.contrib import admin
from .models import Post, Tag, Comment


# ---------------------------
# Post Admin
# ---------------------------
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "author",
        "category",
        "status",
        "file_type",
        "views_count",
        "created_at",
    )

    list_filter = (
        "status",
        "category",
        "file_type",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "author__username",
        "author__first_name",
        "author__last_name",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    ordering = ("-created_at",)

    filter_horizontal = (
        "tags",
        "likes",
        "saves",
    )

    readonly_fields = (
        "views_count",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Basic Info", {
            "fields": (
                "title",
                "slug",
                "author",
                "description",
            )
        }),
        ("Classification", {
            "fields": (
                "category",
                "tags",
                "status",
            )
        }),
        ("Content", {
            "fields": (
                "file_type",
                "image",
                "file",
                "link_url",
            )
        }),
        ("Engagement", {
            "fields": (
                "likes",
                "saves",
                "views_count",
            )
        }),
        ("Timestamps", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )


# ---------------------------
# Tag Admin
# ---------------------------
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    search_fields = (
        "name",
    )
    ordering = (
        "name",
    )


# ---------------------------
# Comment Admin
# ---------------------------
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "post",
        "author",
        "created_at",
    )

    search_fields = (
        "post__title",
        "author__username",
        "author__first_name",
        "author__last_name",
        "content",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
    )