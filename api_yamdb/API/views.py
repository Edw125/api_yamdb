from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination

from API.serializers import CommentSerializer

from reviews.models import Comment


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        if get_object_or_404(Comment, pk=review_id):
            return Comment.objects.filter(post=review_id)
