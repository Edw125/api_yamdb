
# api/urls.py
from django.urls import include, path

from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView
from API.views import GenresViewSet, TitlesViewSet, СategoriesViewSet
from .views import AdminViewSet, RegisterView, UserView, get_token

router_v1 = SimpleRouter()
router_v1.register('users', AdminViewSet)
router_v1.register(r'titles',
                   TitlesViewSet,
                   basename='titles'
                   )
router_v1.register(r'genres',
                   GenresViewSet, 
                   basename='genres'
                   )
router_v1.register(r'categories',
                   СategoriesViewSet,
                   basename='categories'
                   )

urlpatterns = [
    path('v1/auth/token/', get_token, name='get_token'),
    path(
        'v1/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'v1/auth/signup/',
        RegisterView.as_view(),
        name='auth_register'
    ),
    path('v1/users/me/', UserView.as_view(), name='user_me'),
    path('v1/', include(router_v1.urls)),
]
