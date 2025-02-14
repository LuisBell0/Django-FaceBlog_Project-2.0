from rest_framework import serializers

from posts.models import Comment, LikePost, Post, LikeComment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'owner', 'description', 'post_image', 'likes_count', 'comments_count', 'posted_date']


class LikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikePost
        fields = ['id', 'user', 'post', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id', 'user', 'post', 'text', 'likes_count', 'posted_date', 'parent_comment',
        ]


class LikeCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeComment
        fields = ['id', 'user', 'post', 'created_at']
