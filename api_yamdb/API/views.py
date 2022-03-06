from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions, status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from titles.models import Genres, Сategories, Titles
from .permissions import OnlyAdmin, AuthUser
from .serializers import (AdminUserSerializer, GetTokenSerializer,
                          RegisterSerializer, User, UserSerializer,
                          GenresSerializer, СategoriesSerializer,
                          TitlesSerializer,
                          )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token(request):
    serializer = GetTokenSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer = GetTokenSerializer(data=serializer.data)
    if serializer.is_valid():
        data = {'token': serializer.data.get('token')}
        return Response(data, status=status.HTTP_200_OK)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_200_OK)


class AdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = (permissions.IsAuthenticated, OnlyAdmin)
    pagination_class = PageNumberPagination

    @action(
        methods=['get', 'patch', 'delete'],
        detail=False,
        url_path=r'(?P<username>\w+)'
    )
    def admin_functions(self, request, username):
        user = get_object_or_404(User, username=username)
        if request.method == 'GET':
            serializer = AdminUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            data = request.data.copy()
            data['username'] = user.username
            data['email'] = user.email
            serializer = AdminUserSerializer(user, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class UserView(APIView):
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


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
