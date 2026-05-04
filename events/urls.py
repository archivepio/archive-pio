from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, EventTypeViewSet

router = DefaultRouter()
router.register('events', EventViewSet, basename='event')
router.register('event-types', EventTypeViewSet, basename='eventtype')

urlpatterns = [
    path('', include(router.urls)),
]
