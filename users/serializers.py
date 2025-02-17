from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'user',
            'follows',
            'profile_picture',
            'bio',
            'gender',
            'date_of_birth',
            'date_joined',
        ]
