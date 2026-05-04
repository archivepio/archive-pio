from rest_framework import viewsets, permissions
from .models import Event, EventType
from .serializers import EventSerializer, EventTypeSerializer
from logs.utils import log_action


class EventTypeViewSet(viewsets.ModelViewSet):
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()
        log_action(self.request.user, 'CREATE EVENT',
                   f'Created event: {instance.event_title}')

    def perform_update(self, serializer):
        instance = serializer.save()
        log_action(self.request.user, 'UPDATE EVENT',
                   f'Updated event: {instance.event_title}')

    def perform_destroy(self, instance):
        log_action(self.request.user, 'DELETE EVENT',
                   f'Deleted event: {instance.event_title}')
        instance.delete()
