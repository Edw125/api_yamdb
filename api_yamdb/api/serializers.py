import random
import string

from django.core.mail import send_mail
from django.db.models import Avg
from rest_framework import exceptions, filters, serializers
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from reviews.models import Comment, Review

from titles.models import Genres, Categories, Titles


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
                fields=['username', 'email']
            )
        ]

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Недопустимое имя пользователя'
            )
        return value

    def create(self, validated_data):
        letters_and_digits = string.ascii_letters + string.digits
        confirmation_code = ''.join(random.sample(letters_and_digits, 16))
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


class GenresCustomSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Genres
        fields = ('name', 'slug',)


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('name', 'slug',)


class CategoriesCustomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('name', 'slug',)


class TitlesSerializer(serializers.ModelSerializer):
    genre = GenresCustomSerializer(many=True, required=False)
    category = CategoriesCustomSerializer(required=False)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Titles
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category',
        )

    def get_rating(self, obj):
        return obj.reviews.all().aggregate(Avg('score'))['score__avg']


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
