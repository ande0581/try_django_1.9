from django.contrib import admin

# Register your models here.
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'updated', 'timestamp']  # this is what is displayed in the django admin page
    list_filter = ['updated', 'timestamp']  # allows you to filter on these values
    list_display_links = ['content']  # the field you click on to see the record
    search_fields = ['title', 'content']  # the fields you are searching against
    list_editable = ['title']  # allow you to edit the title without going into the record

    class Meta:
        model = Post

admin.site.register(Post, PostAdmin)

