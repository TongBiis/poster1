from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'post_title', 'post_time_create', 'cat', 'vvv')
    list_display_links = ('id', 'post_title')
    list_filter = ('post_time_create',)
    search_fields = ('post_title', 'post_content')
    # prepopulated_fields = {'post_slug': ('post_title',)}


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name')
    list_display_links = ('id', 'category_name')
    list_filter = ('category_name',)
    search_fields = ('id', 'category_name')
    prepopulated_fields = {'slug': ('category_name',)}


class CommentReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'parent_comment', 'reply_content')
    list_display_links = ('id', 'parent_comment', 'reply_content')
    search_fields = ('parent_comment', 'reply_content')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment_create', 'post_comment', 'parent')
    list_display_links = ('id', 'post_comment')
    search_fields = ('id', 'post_comment')


admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(CommentReply, CommentReplyAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(UserIp)

# admin.site.register(Hit)
