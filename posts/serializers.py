from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'owner', 'description', 'post_image', 'likes_count', 'comments_count', 'posted_date']
