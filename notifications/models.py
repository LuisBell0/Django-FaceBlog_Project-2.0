from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser


class NotificationType(models.TextChoices):
    LIKE_COMMENT = 'like_comment', _('Like Comment')
    LIKE_POST = 'like_post', _('Like Post')
    COMMENT_POST = 'comment_post', _('Comment on Post')
    COMMENT_REPLY = 'comment_reply', _('Reply to Comment')
    FOLLOW = 'follow', _('Follow')


class Notification(models.Model):
    message = models.CharField(max_length=255)
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications_received')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications_sent')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=20, choices=NotificationType.choices)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.sender} | {self.notification_type} | {self.created_at}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.cleanup_notifications()

    @staticmethod
    def send_notification(sender, receiver, content_type=None, object_id=None, notification_type=None):
        if sender == receiver:
            return None

        message_map = {
            NotificationType.LIKE_COMMENT: _("liked your comment"),
            NotificationType.LIKE_POST: _("liked your post"),
            NotificationType.COMMENT_POST: _("commented on your post"),
            NotificationType.COMMENT_REPLY: _("replied to your comment"),
            NotificationType.FOLLOW: _("started following you"),
        }
        message = message_map.get(notification_type, "")
        notification = Notification(
            sender=sender,
            receiver=receiver,
            content_type=content_type,
            object_id=object_id,
            notification_type=notification_type,
            message=message
        )
        notification.save()
        return notification

    @classmethod
    def cleanup_notifications(cls):
        max_notifications = 100
        total_count = cls.objects.count()
        if total_count > max_notifications:
            excess_count = total_count - max_notifications
            old_notifications = cls.objects.order_by('created_at')[:excess_count].values_list('id', flat=True)
            cls.objects.filter(id__in=list(old_notifications)).delete()
