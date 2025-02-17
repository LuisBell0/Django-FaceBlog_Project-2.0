from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django_faceblog.permissions import IsUserOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsUserOrReadOnly]

    def get_related_profiles(self, profile_id, relation_field):
        """Helper function to retrieve related profiles dynamically."""
        profile = get_object_or_404(Profile, id=profile_id)
        related_profiles = getattr(profile, relation_field).all()
        return self.get_serializer(related_profiles, many=True).data

    @action(detail=False, methods=['GET'], url_path='followers/(?P<profile_id>[^/.]+)')
    def get_followers(self, request, profile_id=None):
        """Returns the profiles following the given profile."""
        return Response(self.get_related_profiles(profile_id, 'followed_by'))

    @action(detail=False, methods=['GET'], url_path='following/(?P<profile_id>[^/.]+)')
    def get_following(self, request, profile_id=None):
        """Returns the profiles that the given profile is following."""
        return Response(self.get_related_profiles(profile_id, 'follows'))
