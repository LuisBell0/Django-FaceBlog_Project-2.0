from django.contrib.auth.models import AbstractUser
from django.db import models
from django_faceblog.utils import compress_image


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=100)


def user_profile_picture_path(instance, filename):
    return f'users/profile_pictures/{instance.user.username}/{filename}'


class Profile(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self',
                                     related_name='followed_by', symmetrical=False, blank=True)
    profile_picture = models.ImageField(upload_to=user_profile_picture_path,
                                        blank=True, null=True)
    bio = models.TextField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_joined = models.DateField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        if self.profile_picture:
            self.profile_picture = compress_image(self.profile_picture)
        super().save(*args, **kwargs)

    def get_followers_count(self):
        return self.followed_by.count() - 1

    def get_following_count(self):
        return self.follows.count() - 1
