from django.contrib import admin, messages

from women.models import Women, Category


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    list_display = ("title", "time_create", "is_published", "cat", "brief_info")
    list_display_links = ("title",)
    ordering = ["-time_create", "title"]
    list_editable = ["is_published"]
    list_per_page = 5
    actions = ["set_published", "set_draft"]

    @admin.display(description="Brief description", ordering="content")
    def brief_info(self, women: Women):
        return f"Описание {len(women.content)} символов."

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
