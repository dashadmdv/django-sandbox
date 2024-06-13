from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, BaseValidator
from django.utils.deconstruct import deconstructible

from women.models import Category, Husband


@deconstructible
class RussianValidator(BaseValidator):
    ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
    code = "russian"

    def __init__(self, message=None):
        self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел."

    def __call__(self, value, *args, **kwargs):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)


class AddPostForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        min_length=5,
        label="Title",
        widget=forms.TextInput(attrs={"class": "form-input"}),
        # validators=[RussianValidator()],
        error_messages={
            "min_length": "Title is too short!",
            "required": "No title!",
        },
    )
    slug = forms.SlugField(
        max_length=255,
        label="URL",
        validators=[
            MinLengthValidator(5, message="Minimum 5 symbols"),
            MaxLengthValidator(100, "Maximum 100 symbols"),
        ],
    )
    content = forms.CharField(widget=forms.Textarea(attrs={"cols": 50, "rows": 5}), required=False, label="Content")
    is_published = forms.BooleanField(required=False, initial=True, label="Status")
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Category not chosen", label="Categories")
    husband = forms.ModelChoiceField(
        queryset=Husband.objects.all(), required=False, empty_label="Not married", label="Husband"
    )

    def clean_title(self):
        title = self.cleaned_data["title"]
        ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
        if not (set(title) <= set(ALLOWED_CHARS)):
            raise ValidationError("Должны присутствовать только русские символы, дефис и пробел.")
