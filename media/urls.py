from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FileTypeViewSet, MediaFileViewSet

router = DefaultRouter()
router.register('file-types', FileTypeViewSet, basename='filetype')
router.register('media-files', MediaFileViewSet, basename='mediafile')

urlpatterns = [
    path('', include(router.urls)),
]
