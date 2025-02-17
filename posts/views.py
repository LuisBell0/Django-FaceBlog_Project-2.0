from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django_faceblog.permissions import IsUserOrReadOnly
from posts.models import Comment, LikePost, Post, LikeComment
from posts.serializers import CommentSerializer, LikePostSerializer, PostSerializer, LikeCommentSerializer
from .mixins import FilterByPostMixin
from .permissions import IsOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def list(self, request, *args, **kwargs):
        current_user = self.request.user
        posts = Post.objects.filter(owner=current_user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='following-posts/(?P<profile_id>[^/.]+)')
    def user_following_posts(self, request, profile_id=None):
        queryset = self.get_queryset().filter(
            Q(owner=request.user) | Q(owner__profile__followed_by=profile_id)
        ).prefetch_related('owner').distinct()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LikePostViewSet(FilterByPostMixin, viewsets.ModelViewSet):
    queryset = LikePost.objects.all()
    serializer_class = LikePostSerializer
    permission_classes = [IsAuthenticated, IsUserOrReadOnly]


class CommentViewSet(FilterByPostMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsUserOrReadOnly]

    @action(detail=False, methods=['GET'], url_path='comment/(?P<comment_id>[^/.]+)')
    def comment_replies(self, request, comment_id=None):
        queryset = self.get_queryset().filter(parent_comment_id=comment_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LikeCommentViewSet(FilterByPostMixin, viewsets.ModelViewSet):
    queryset = LikeComment.objects.all()
    serializer_class = LikeCommentSerializer
    permission_classes = [IsAuthenticated, IsUserOrReadOnly]
