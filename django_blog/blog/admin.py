from django.contrib import admin
from .models import Post, Comment, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_post_count')
    search_fields = ('name',)
    ordering = ('name',)
    
    def get_post_count(self, obj):
        return obj.posts.count()
    get_post_count.short_description = 'Number of Posts'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'get_tag_list')
    list_filter = ('published_date', 'author', 'tags')
    search_fields = ('title', 'content')
    date_hierarchy = 'published_date'
    filter_horizontal = ('tags',)
    
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
