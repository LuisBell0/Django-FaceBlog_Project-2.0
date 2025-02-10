from io import BytesIO
from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.files.base import ContentFile


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)


class Profile(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self',
                                     related_name='followed_by', symmetrical=False, blank=True)
    profile_picture = models.ImageField(upload_to="users/profile_pictures/",
                                        blank=True, null=True)
    bio = models.TextField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_joined = models.DateField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.profile_picture:
            img = Image.open(self.profile_picture)
            img_format = img.format

            if img_format in ['JPEG', 'PNG', 'JPG']:
                img = img.convert('RGB')
                buffer = BytesIO()
                img.save(buffer, format='JPEG' if img_format in ["JPEG", "JPG"] else "PNG", quality=70, optimize=True)
                self.profile_picture.save(self.profile_picture.name, ContentFile(buffer.getvalue()), save=False)

    def get_followers_count(self):
        return self.followed_by.count() - 1

    def get_following_count(self):
        return self.follows.count() - 1
