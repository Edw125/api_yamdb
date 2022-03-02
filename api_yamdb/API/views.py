
from django.contrib.auth import get_user_model
from rest_framework import filters, status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from titles.models import Genres, Сategories, Titles


from .permissions import AuthUser
from .serializers import (GenresSerializer, СategoriesSerializer, TitlesSerializer)


# from user.models import User

User = get_user_model()


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    pagination_class = LimitOffsetPagination
    
    def perform_create(self, serializer):
        user_del = self.request.user # Проверка прав доступа Адмнистратор !НЕДОДЕЛАНО!
        author = self.request.user  # Проверка прав доступа Адмнистратор !НЕДОДЕЛАНО!
        if user_del != author: # Проверка прав доступа Адмнистратор !НЕДОДЕЛАНО!
            raise PermissionDenied('Добавлять Жанры может только Адмнистратор')
        serializer.save()

    def perform_update(self, serializer):
        user_upd = self.request.user  # Проверка прав доступа Адмнистратор !НЕДОДЕЛАНО!
        author = self.request.user  # Проверка прав доступа Адмнистратор !НЕДОДЕЛАНО!
        if user_upd != author:  # Проверка прав доступа Адмнистратор !НЕДОДЕЛАНО!
            raise PermissionDenied('Изменять Жанры может только Адмнистратор')
        serializer.save()
        
    def perform_destroy(self, serializer):
        instance = self.get_object()
        user_upd = self.request.user  # Проверка прав доступа Адмнистратор !НЕДОДЕЛАНО!
        author = self.request.user  # Проверка прав доступа Адмнистратор !НЕДОДЕЛАНО!
        if user_upd != author:  # Проверка прав доступа Адмнистратор !НЕДОДЕЛАНО!
            raise PermissionDenied('Удалять Жанры может только Адмнистратор')
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    pagination_class = LimitOffsetPagination
    
    def perform_create(self, serializer):
        user_del = self.request.user # Проверка прав доступа Адмнистратор !НЕДОДЕЛАНО!
        author = self.request.user  # Проверка прав доступа Адмнистратор !НЕДОДЕЛАНО!
        if user_del != author: # Проверка прав доступа Адмнистратор !НЕДОДЕЛАНО!
            raise PermissionDenied('Добавлять Произведения может только Адмнистратор')
        serializer.save()

    def perform_update(self, serializer):
        user_upd = self.request.user  # Проверка прав доступа Адмнистратор !НЕДОДЕЛАНО!
        author = self.request.user  # Проверка прав доступа Адмнистратор !НЕДОДЕЛАНО!
        if user_upd != author:  # Проверка прав доступа Адмнистратор !НЕДОДЕЛАНО!
            raise PermissionDenied('Изменять Произведения может только Адмнистратор')
        serializer.save()
        
    def perform_destroy(self, serializer):
        instance = self.get_object()
        user_upd = self.request.user  # Проверка прав доступа Адмнистратор !НЕДОДЕЛАНО!
        author = self.request.user  # Проверка прав доступа Адмнистратор !НЕДОДЕЛАНО!
        if user_upd != author:  # Проверка прав доступа Адмнистратор !НЕДОДЕЛАНО!
            raise PermissionDenied('Удалять Произведения может только Адмнистратор')
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class СategoriesViewSet(viewsets.ModelViewSet):
    queryset = Сategories.objects.all()
    serializer_class = СategoriesSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        user_del = self.request.user # Проверка прав доступа Адмнистратор !НЕДОДЕЛАНО!
        author = self.request.user  # Проверка прав доступа Адмнистратор !НЕДОДЕЛАНО!
        if user_del != author: # Проверка прав доступа Адмнистратор !НЕДОДЕЛАНО!
            raise PermissionDenied('Добавлять Категории может только Адмнистратор')
        serializer.save()

    def perform_update(self, serializer):
        user_upd = self.request.user  # Проверка прав доступа Адмнистратор !НЕДОДЕЛАНО!
        author = self.request.user  # Проверка прав доступа Адмнистратор !НЕДОДЕЛАНО!
        if user_upd != author:  # Проверка прав доступа Адмнистратор !НЕДОДЕЛАНО!
            raise PermissionDenied('Изменять Категории может только Адмнистратор')
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, serializer):
        instance = self.get_object()
        user_upd = self.request.user  # Проверка прав доступа Адмнистратор !НЕДОДЕЛАНО!
        author = self.request.user  # Проверка прав доступа Адмнистратор !НЕДОДЕЛАНО!
        if user_upd != author:  # Проверка прав доступа Адмнистратор !НЕДОДЕЛАНО!
            raise PermissionDenied('Удалять Категории может только Адмнистратор')
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
