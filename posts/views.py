from django.db.models import Q
from rest_framework.exceptions import NotFound, AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework import viewsets

from posts.models import Post
from posts.serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request):
        current_user = self.request.user

        if not current_user.is_authenticated:
            raise AuthenticationFailed("Authentication credentials were not provided.")

        posts = Post.objects.filter(owner=current_user)
        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserFollowingPostsListAPIView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        current_user = self.request.user

        # Check if the user is authenticated
        if not current_user.is_authenticated:
            raise AuthenticationFailed("Authentication credentials were not provided.")

        # Get the user's profile
        user_profile = getattr(current_user, 'profile', None)
        if user_profile is None:
            raise NotFound("User profile does not exist.")

        # Query for the user's posts and the posts from followed profiles
        query = Post.objects.filter(
            Q(owner=current_user) | Q(owner__profile__followed_by=user_profile)
        ).prefetch_related('owner').distinct()
        return query

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
