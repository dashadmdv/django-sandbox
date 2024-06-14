from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from women.models import Women, Category


class MarriedFilter(admin.SimpleListFilter):
    title = "Women status"
    parameter_name = "status"

    def lookups(self, request, model_admin):
        return [
            ("married", "Married"),
            ("single", "Not married"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "married":
            return queryset.filter(husband__isnull=False)
        elif self.value() == "single":
            return queryset.filter(husband__isnull=True)


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    fields = ["title", "content", "photo", "post_photo", "slug", "cat", "husband", "tags"]
    # exclude = ["tags", "is_published"]
    readonly_fields = ["post_photo"]
    prepopulated_fields = {"slug": ("title",)}
    # filter_horizontal = ["tags"]
    filter_vertical = ["tags"]
    list_display = ("title", "post_photo", "time_create", "is_published", "cat")
    list_display_links = ("title",)
    ordering = ["-time_create", "title"]
    list_editable = ["is_published"]
    list_per_page = 5
    actions = ["set_published", "set_draft"]
    search_fields = ["title", "cat__name"]
    list_filter = [MarriedFilter, "cat__name", "is_published"]
    save_on_top = True

    @admin.display(description="Image", ordering="content")
    def post_photo(self, women: Women):
        if women.photo:
            return mark_safe(f"<img src='{women.photo.url}' width=50>")
        return "Without photo"

    @admin.action(description="Publish")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=1)
        self.message_user(request, f"Changed {count} entries")

    @admin.action(description="Unpublish")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=0)
        self.message_user(request, f"Drafted {count} entries", messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")


# admin.site.register(Women, WomenAdmin)
