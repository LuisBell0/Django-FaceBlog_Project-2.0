import os
from PIL import Image, ImageOps
from django.core.exceptions import ValidationError
from django.db import models
from users.models import CustomUser


class Post(models.Model):
    owner = models.ForeignKey(CustomUser,
                              on_delete=models.CASCADE,
                              related_name="posts")
    description = models.TextField(blank=True, max_length=255)
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    posted_date = models.DateTimeField(auto_now_add=True)
    post_image = models.ImageField(upload_to='posts/post/', blank=True, null=True)

    def __str__(self):
        return f'{self.owner}, {self.description}, {self.posted_date}'

    def clean(self):
        if not self.description and not self.img:
            raise ValidationError('You must provide either a description or an image.')

    def delete(self, *args, **kwargs):
        # Delete the associated image file from the filesystem
        if self.post_image:
            if os.path.isfile(self.post_image.path):
                os.remove(self.post_image.path)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.post_image:
            try:
                img = Image.open(self.post_image.path)

                # Correct orientation based on EXIF data
                img = ImageOps.exif_transpose(img)

                # Save the image with appropriate compression
                if img.format == 'JPEG':
                    img.save(self.post_image.path, format='JPEG', quality=70)  # Compress JPEG
                elif img.format == 'PNG':
                    img.save(self.post_image.path, format='PNG', optimize=True)  # Compress PNG
            except Exception as e:
                print(f"Image processing error: {e}")


class LikePost(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # Ensures one like per user per post

    def __str__(self):
        return f'{self.user} | {self.post}'


class Comment(models.Model):
    text = models.CharField(max_length=255)
    likes_count = models.PositiveIntegerField(default=0)
    posted_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    parent_comment = models.ForeignKey('self',
                                       on_delete=models.CASCADE,
                                       null=True,
                                       blank=True,
                                       related_name='replies')

    class Meta:
        ordering = ['-posted_date']

    def __str__(self):
        return f'{self.user} | {self.post} | {self.posted_date}'


class LikeComment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment')  # Ensures one like per user per post

    def __str__(self):
        return f'{self.user} | {self.comment}'
