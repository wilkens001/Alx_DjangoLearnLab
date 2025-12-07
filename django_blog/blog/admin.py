from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'get_tag_list')
    list_filter = ('published_date', 'author')
    search_fields = ('title', 'content', 'tags__name')
    date_hierarchy = 'published_date'
    
    def get_tag_list(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    get_tag_list.short_description = 'Tags'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'author')
    search_fields = ('content', 'author__username', 'post__title')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
