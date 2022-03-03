import random
import string
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    

    class Meta:
        model = User
        fields = ('email', 'username',)

    def create(self, validated_data):
        letters_and_digits = string.ascii_letters + string.digits
        confirmation_code = ''.join(random.sample(letters_and_digits, 16))
        confirmation_message = (
            f'Здравствуйте! Спасибо за регистрацию в проекте YaMDb. ',
            f'Ваш код подтверждения: ${confirmation_code}. ',
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
