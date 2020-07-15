from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MapViewSet, UserViewSet, GameStateViewSet

router = DefaultRouter()
router.register('user', UserViewSet)
router.register('map', MapViewSet)
router.register('game-state', GameStateViewSet)