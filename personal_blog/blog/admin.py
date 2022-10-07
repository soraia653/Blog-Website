from gettext import ngettext
from django.contrib import admin, messages
from django.utils.translation import ngettext
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display=['title', 'author', 'status', 'published_date']
    prepopulated_fields={'slug_title':('title',)}
    actions=['make_published']

    @admin.action(description="Mark selected posts as published.")
    def make_published(self, request, queryset):
        updated = queryset.update(status=True)

        self.message_user(request, ngettext(
            '%d post was successfully marked as published!',
            '%d posts were successfully marked as published!',
            updated,
        ) % updated, messages.SUCCESS)

# Register your models here.
admin.site.register(Post, PostAdmin)
