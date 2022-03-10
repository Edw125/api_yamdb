from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, generics, mixins, permissions, status,
                            viewsets)
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)

from rest_framework.response import Response
from rest_framework.views import APIView

from reviews.models import Comment, Review
from titles.models import Categories, Genres, Title
from users.models import User
from .filters import TitleFilter
from .permissions import (IsAdminOrReadOnlyAnonymusPermission, OnlyAdmin,
                          ReviewAndCommentPermission)
from .serializers import (AdminUserSerializer, CategoriesSerializer,
                          CommentSerializer, GenresSerializer,
                          GetTokenSerializer, RegisterSerializer,
                          ReviewSerializer, TitlesSerializer, UserSerializer)


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


class GetListCreateDeleteViewSet(mixins.ListModelMixin,
                                 mixins.CreateModelMixin,
                                 mixins.DestroyModelMixin,
                                 viewsets.GenericViewSet):
    pass


class GenresViewSet(GetListCreateDeleteViewSet):
    lookup_field = 'slug'
    queryset = Genres.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    serializer_class = GenresSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnlyAnonymusPermission,)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitlesSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnlyAnonymusPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter


class CategoriesViewSet(GetListCreateDeleteViewSet):
    lookup_field = 'slug'
    queryset = Categories.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    serializer_class = CategoriesSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnlyAnonymusPermission,)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (ReviewAndCommentPermission,)
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        if not Review.objects.filter(id=review_id).exists():
            raise NotFound()
        review = Review.objects.get(id=review_id)
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        if not Review.objects.filter(id=review_id).exists():
            raise NotFound()
        return Comment.objects.filter(review=review_id)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (ReviewAndCommentPermission,)
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        if not Title.objects.filter(id=title_id).exists():
            raise NotFound()
        title = Title.objects.get(id=title_id)
        existing = Review.objects.filter(
            author=self.request.user,
            title=title
        ).exists()
        if existing:
            raise ParseError()
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        if get_object_or_404(Title, pk=title_id):
            return Review.objects.filter(title=title_id)
