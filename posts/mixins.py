from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class FilterByPostMixin:
    """
    A reusable mixin to filter likes by post ID.
    """
    @action(detail=False, methods=['GET'], url_path='post/(?P<post_id>[^/.]+)')
    def list_by_post(self, request, post_id=None):
        queryset = self.get_queryset().filter(post=post_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
