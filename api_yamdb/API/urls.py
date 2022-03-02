from API.views import GenresViewSet, TitlesViewSet, СategoriesViewSet
from django.urls import include, path
from rest_framework import routers

router_v1 = routers.DefaultRouter()
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

    path('v1/', include(router_v1.urls)),
]