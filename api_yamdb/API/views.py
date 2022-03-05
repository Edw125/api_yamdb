from django.shortcuts import get_object_or_404

from rest_framework import permissions

from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets

from .serializers import User, RegisterSerializer, GetTokenSerializer, UserSerializer

from rest_framework import generics

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token(request):
    serializer = GetTokenSerializer(data=request.data)
    if serializer.is_valid():
        serializer = GetTokenSerializer(data=serializer.data)
    if serializer.is_valid():
        data = {'token': serializer.data.get('token')}
        return Response(data, status=status.HTTP_200_OK)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
        methods=['get'],
        detail=False,
        url_path='(?P<username>\w+)'
    )
    def getByUsername(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

