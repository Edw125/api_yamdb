from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination

from API.serializers import CommentSerializer, ReviewSerializer

from reviews.models import Comment, Review


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        if not get_object_or_404(Review, pk=review_id):
            raise PermissionDenied(
                'Невозможно создать комментарий к несуществующему отзыву!'
            )
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        super(CommentViewSet, self).perform_destroy(instance)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        if get_object_or_404(Comment, pk=review_id):
            return Comment.objects.filter(review=review_id)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(ReviewViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        super(ReviewViewSet, self).perform_destroy(instance)
