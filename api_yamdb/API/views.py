
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


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    pagination_class = LimitOffsetPagination
    

class СategoriesViewSet(viewsets.ModelViewSet):
    queryset = Сategories.objects.all()
    serializer_class = СategoriesSerializer
    pagination_class = LimitOffsetPagination