import datetime as dt
import uuid

from django.core.mail import send_mail
from django.db.models import Avg
from rest_framework import exceptions, filters, serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Comment, Review
from titles.models import Categories, Genres, Title
from users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('email', 'username',)
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email')
            )
        ]

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Недопустимое имя пользователя'
            )
        return value

    def create(self, validated_data):
        confirmation_code = str(uuid.uuid4())
        confirmation_message = (
            'Здравствуйте! Спасибо за регистрацию в проекте YaMDb. ',
            f'Ваш код подтверждения: {confirmation_code}. ',
            'Он вам понадобится для получения токена для работы с Api YaMDb.',
            'Токен можно получить по ссылке: ',
            'http://127.0.0.1:8000/api/v1/auth/token/'
        )
        email = validated_data['email']
        username = validated_data['username']

        send_mail(
            'Код подтверждения регистрации',
            f'{confirmation_message}',
            'from@example.com',
            [email],
        )

        user = User.objects.create(
            username=username,
            email=email,
            confirmation_code=confirmation_code
        )
        return user


class GetTokenSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    username = serializers.CharField(
        max_length=150,
        allow_blank=False,
    )
    confirmation_code = serializers.CharField(
        max_length=150,
        allow_blank=False,
    )
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'confirmation_code', 'token')

    def validate(self, data):
        existing = User.objects.filter(
            username=data['username'],
        ).exists()
        if not existing:
            raise exceptions.NotFound("Пользователь не найден")
        user = User.objects.get(username=data['username'])
        if user.confirmation_code != data['confirmation_code']:
            raise exceptions.ParseError("Код подтверждения не верный")
        return data

    def get_token(self, obj):
        username = list(obj.items())[0][1]
        confirmation_code = list(obj.items())[1][1]
        user = User.objects.get(
            username=username,
            confirmation_code=confirmation_code
        )
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def get_id(self, obj):
        username = list(obj.items())[0][1]
        user = User.objects.get(username=username)
        return user.id


class AdminUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]
        filter_backends = (filters.SearchFilter,)
        search_fields = ('username',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        read_only_fields = ('role', 'username', 'email')


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('name', 'slug',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('name', 'slug',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreField(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = GenresSerializer(value)
        return serializer.data


class CategoryField(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = CategoriesSerializer(value)
        return serializer.data


class TitlesSerializer(serializers.ModelSerializer):
    genre = GenreField(slug_field='slug',
                       queryset=Genres.objects.all(),
                       many=True
                       )
    category = CategoryField(slug_field='slug',
                             queryset=Categories.objects.all()
                             )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category',
        )
        filter_backends = (filters.SearchFilter,)
        search_fields = ('genre',)

    def get_rating(self, obj):
        return obj.reviews.all().aggregate(Avg('score'))['score__avg']

    def validate_year(self, value):
        kw_data = self._kwargs['data']
        category = kw_data['category']
        if category == 'movie':
            year = dt.date.today().year
            start_year = 1895
            error_msg = 'Проверьте год создания произведения!'
            if not (start_year < value <= year):
                raise serializers.ValidationError(error_msg)
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
        read_only_fields = ('id', 'pub_date',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        model = Review
        read_only_fields = ('id', 'pub_date',)
