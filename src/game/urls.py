from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MapViewSet, UserViewSet, GameStateViewSet, login, get_access_token

router = DefaultRouter()
router.register('user', UserViewSet)
router.register('map', MapViewSet)
router.register('game-state', GameStateViewSet)

urlpatterns = [
  path('login', login),
  path('acquireaccesstoken', get_access_token),
  path('', include(router.urls))
]