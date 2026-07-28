from django import forms
from .models import Post, Comment, Tag


class PostCreateForm(forms.ModelForm):
    """
    Used for upload.html
    Handles image / pdf / ebook / link uploads
    Tags are handled as comma-separated input
    """

    tags = forms.CharField(
        required=False,
        help_text="Comma separated tags (e.g. math, algebra, notes)"
    )

    class Meta:
        model = Post
        fields = [
            "title",
            "description",
            "category",
            "image",
            "file",
            "link_url",
        ]

        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Post title"}),
            "description": forms.Textarea(attrs={"rows": 4}),
            "category": forms.Select(),
            "link_url": forms.URLInput(attrs={"placeholder": "https://example.com"}),
        }

    def clean(self):
        """
        Ensure at least one content source is provided
        """
        cleaned_data = super().clean()

        image = cleaned_data.get("image")
        file = cleaned_data.get("file")
        link_url = cleaned_data.get("link_url")

        if not image and not file and not link_url:
            raise forms.ValidationError(
                "You must upload an image, a file, or provide a link."
            )

        return cleaned_data

    def save(self, commit=True, author=None, status="published"):
        """
        Custom save to:
        - assign author
        - set status (published / draft)
        - auto-detect file_type
        - handle tags
        """
        post = super().save(commit=False)

        # Assign author
        if author:
            post.author = author

        # Set post status
        post.status = status

        # Detect file type
        if post.image:
            post.file_type = "image"
        elif post.file:
            filename = post.file.name.lower()
            if filename.endswith(".pdf"):
                post.file_type = "pdf"
            elif filename.endswith((".epub", ".mobi")):
                post.file_type = "ebook"
            else:
                post.file_type = "other"
        elif post.link_url:
            post.file_type = "link"
        else:
            post.file_type = "other"

        if commit:
            post.save()

            # Handle tags
            tags_raw = self.cleaned_data.get("tags", "")
            if tags_raw:
                tag_names = [
                    t.strip().lower()
                    for t in tags_raw.split(",")
                    if t.strip()
                ]

                for name in tag_names:
                    tag, _ = Tag.objects.get_or_create(name=name)
                    post.tags.add(tag)

        return post


class CommentForm(forms.ModelForm):
    """
    Used in post_detail.html
    """

    class Meta:
        model = Comment
        fields = ["content"]

        widgets = {
            "content": forms.Textarea(
                attrs={
                    "placeholder": "Write your comment...",
                    "rows": 3,
                }
            )
        }