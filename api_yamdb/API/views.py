from rest_framework import viewsets , permissions

from .serializers import User, RegisterSerializer

from rest_framework import generics


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer