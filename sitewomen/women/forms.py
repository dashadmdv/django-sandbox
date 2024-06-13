from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible

from women.models import Women, Category, Husband


@deconstructible
class RussianValidator(BaseValidator):
    ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
    code = "russian"

    def __init__(self, message=None):
        self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел."

    def __call__(self, value, *args, **kwargs):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)


class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Category not chosen", label="Categories")
    husband = forms.ModelChoiceField(
        queryset=Husband.objects.all(), required=False, empty_label="Not married", label="Husband"
    )

    class Meta:
        model = Women
        fields = ["title", "slug", "content", "is_published", "cat", "husband", "tags"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input"}),
            "content": forms.Textarea(attrs={"cols": 50, "rows": 5}),
        }
        labels = {"slug": "URL"}

    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) > 50:
            raise ValidationError("Длина превышает 50 символов")

        return title
