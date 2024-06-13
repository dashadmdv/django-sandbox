from django.db import models
from django.urls import reverse


# def translit_to_eng(s: str) -> str:
#     d = {
#         "а": "a",
#         "б": "b",
#         "в": "v",
#         "г": "g",
#         "д": "d",
#         "е": "e",
#         "ё": "yo",
#         "ж": "zh",
#         "з": "z",
#         "и": "i",
#         "к": "k",
#         "л": "l",
#         "м": "m",
#         "н": "n",
#         "о": "o",
#         "п": "p",
#         "р": "r",
#         "с": "s",
#         "т": "t",
#         "у": "u",
#         "ф": "f",
#         "х": "h",
#         "ц": "c",
#         "ч": "ch",
#         "ш": "sh",
#         "щ": "shch",
#         "ь": "",
#         "ы": "y",
#         "ъ": "",
#         "э": "r",
#         "ю": "yu",
#         "я": "ya",
#     }
#
#     return "".join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=1)


class Women(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    content = models.TextField(blank=True)
    time_create = models.TimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    cat = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="posts")
    tags = models.ManyToManyField("TagPost", blank=True, related_name="tags")
    husband = models.OneToOneField("Husband", on_delete=models.SET_NULL, null=True, blank=True, related_name="woman")

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

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(translit_to_eng(self.title))
    #     super().save(*args, **kwargs)


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
