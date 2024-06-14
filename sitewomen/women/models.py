from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=1)


class Women(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        validators=[
            MinLengthValidator(5, message="Minimum 5 symbols"),
            MaxLengthValidator(100, "Maximum 100 symbols"),
        ],
    )
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", default=None, blank=True, null=True, verbose_name="Photo")
    content = models.TextField(blank=True)
    time_create = models.TimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    cat = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="posts")
    tags = models.ManyToManyField("TagPost", blank=True, related_name="tags")
    husband = models.OneToOneField("Husband", on_delete=models.SET_NULL, null=True, blank=True, related_name="woman")
    author = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, related_name="posts", null=True, default=None
    )

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-time_create"]
        indexes = [
            models.Index(fields=["-time_create"]),
        ]
        verbose_name = "Woman"
        verbose_name_plural = "Women"

    def get_absolute_url(self):
        return reverse("post", kwargs={"post_slug": self.slug})


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category", kwargs={"cat_slug": self.slug})


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse("tag", kwargs={"tag_slug": self.slug})


class Husband(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    m_count = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.name


class UploadFiles(models.Model):
    file = models.FileField(upload_to="uploads_model")
