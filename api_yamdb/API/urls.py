# api/urls.py
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import SimpleRouter

from django.urls import include, path
from .views import RegisterView, UserViewSet, get_token

router_v1 = SimpleRouter()
router_v1.register('users', UserViewSet)

urlpatterns = [
    path('v1/auth/token/', get_token, name='get_token'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/auth/signup/', RegisterView.as_view(), name='auth_register'),
    path('v1/', include(router_v1.urls)),
]