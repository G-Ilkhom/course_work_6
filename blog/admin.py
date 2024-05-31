from django.contrib import admin
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'publication_date', 'views_count', 'publication_sign')
    search_fields = ('title', 'content')
    list_filter = ('publication_date', 'publication_sign')
    readonly_fields = ('views_count',)
