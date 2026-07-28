from django.conf import settings
from django.db import models
from django.utils.text import slugify

User = settings.AUTH_USER_MODEL


# ---------------------------
# Tag model
# ---------------------------
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


# ---------------------------
# Post model
# ---------------------------
class Post(models.Model):
    CATEGORY_CHOICES = [
        ("mathematics", "Mathematics"),
        ("science", "Science"),
        ("literature", "Literature"),
        ("history", "History"),
        ("programming", "Programming"),
        ("business", "Business"),
        ("design", "Design"),
        ("languages", "Languages"),
        ("other", "Other"),
    ]

    FILE_TYPE_CHOICES = [
        ("image", "Image"),
        ("pdf", "PDF"),
        ("link", "Link"),
        ("ebook", "E-book"),
        ("other", "Other"),
    ]

    STATUS_CHOICES = [
        ("published", "Published"),
        ("draft", "Draft"),
    ]

    # Core
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    description = models.TextField()

    # Classification
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="posts"
    )

    # Content
    file_type = models.CharField(
        max_length=20,
        choices=FILE_TYPE_CHOICES,
        default="other"
    )
    image = models.ImageField(
        upload_to="posts/images/",
        blank=True,
        null=True
    )
    file = models.FileField(
        upload_to="posts/files/",
        blank=True,
        null=True
    )
    link_url = models.URLField(
        blank=True,
        null=True
    )

    # Engagement
    likes = models.ManyToManyField(
        User,
        related_name="liked_posts",
        blank=True
    )
    saves = models.ManyToManyField(
        User,
        related_name="saved_posts",
        blank=True
    )

    views_count = models.PositiveIntegerField(default=0)

    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="published"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    # ---------------------------
    # Computed properties
    # ---------------------------
    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def saves_count(self):
        return self.saves.count()

    @property
    def comments_count(self):
        return self.comments.count()

    def __str__(self):
        return f"{self.title} by {self.author}"


# ---------------------------
# Comment model
# ---------------------------
class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"