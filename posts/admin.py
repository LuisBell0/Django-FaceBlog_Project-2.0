from django.contrib import admin
from .models import Post, LikePost, Comment, LikeComment


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'description', 'posted_date')


class LikePostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'created_at')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'text', 'posted_date')


class LikeCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'comment', 'created_at')


admin.site.register(Post, PostAdmin)
admin.site.register(LikePost, LikePostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(LikeComment, LikeCommentAdmin)
