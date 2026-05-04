from rest_framework import viewsets, permissions
from .models import FileType, MediaFile
from .serializers import FileTypeSerializer, MediaFileSerializer
from logs.utils import log_action


class FileTypeViewSet(viewsets.ModelViewSet):
    queryset = FileType.objects.all()
    serializer_class = FileTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


class MediaFileViewSet(viewsets.ModelViewSet):
    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()
        log_action(self.request.user, 'UPLOAD MEDIA',
                   f'Uploaded media: {instance.file_name}')

    def perform_destroy(self, instance):
        log_action(self.request.user, 'DELETE MEDIA',
                   f'Deleted media: {instance.file_name}')
        instance.delete()
