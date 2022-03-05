import random
import string
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.validators import UniqueTogetherValidator


User = get_user_model()

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
            f'Здравствуйте! Спасибо за регистрацию в проекте YaMDb. ',
            f'Ваш код подтверждения: {confirmation_code}. ',
            f'Он вам понадобится для получения токена для работы с Api YaMDb.',
            f'Токен можно получить по ссылке: ',
            f'http://127.0.0.1:8000/api/v1/auth/token/'
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
    username = serializers.CharField(
        max_length=150,
        allow_blank=False,
    )
    token = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()


    class Meta:
        model = User
        fields = ('id', 'username', 'confirmation_code', 'token')

    def get_token(self, obj):
        username = list(obj.items())[0][1]
        confirmation_code = list(obj.items())[1][1]
        user = User.objects.get(username=username, confirmation_code=confirmation_code)
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def get_id(self, obj):
        username = list(obj.items())[0][1]
        user = User.objects.get(username=username)
        return user.id

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]