from celery import shared_task
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from django.utils import timezone


@shared_task
def flush_expired_tokens():
    """Deletes expired tokens from the database."""
    BlacklistedToken.objects.filter(token__expires_at__lt=timezone.now()).delete()
    OutstandingToken.objects.filter(token__expires_at__lt=timezone.now()).delete()
