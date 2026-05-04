from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (RequesterViewSet, StatusViewSet, PlatformViewSet,
                    RequestViewSet, ApprovalViewSet, AttachmentViewSet,
                    PublicationViewSet, ProcessingLogViewSet)

router = DefaultRouter()
router.register('requesters', RequesterViewSet, basename='requester')
router.register('statuses', StatusViewSet, basename='status')
router.register('platforms', PlatformViewSet, basename='platform')
router.register('requests', RequestViewSet, basename='request')
router.register('approvals', ApprovalViewSet, basename='approval')
router.register('attachments', AttachmentViewSet, basename='attachment')
router.register('publications', PublicationViewSet, basename='publication')
router.register('processing-logs', ProcessingLogViewSet, basename='processinglog')

urlpatterns = [
    path('', include(router.urls)),
]
