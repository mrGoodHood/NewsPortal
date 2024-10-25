from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'post_type', 'created_at', 'rating', 'title', 'text',)
    search_fields = ('text',)
    list_filter = ('author', 'post_type', 'created_at', 'category',)
    empty_value_display = '----'

class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'text', 'created_at', 'rating', 'post',)
    search_fields = ('post', 'user', 'text',)
    list_filter = ('post', 'user', 'created_at', 'rating',)

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Comment)
