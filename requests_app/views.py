from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from .models import (Requester, Status, Platform, Request,
                     Approval, Attachment, Publication, ProcessingLog)
from .serializers import (RequesterSerializer, StatusSerializer,
                          PlatformSerializer, RequestSerializer,
                          ApprovalSerializer, AttachmentSerializer,
                          PublicationSerializer, ProcessingLogSerializer)
from logs.utils import log_action
from notifications.utils import send_notification
from django.contrib.auth import get_user_model
from users.permissions import IsStaffOrAdmin, IsOwnerOrStaff

User = get_user_model()


class RequesterViewSet(viewsets.ModelViewSet):
    queryset = Requester.objects.all()
    serializer_class = RequesterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Requester.objects.all()
        # Citizens only see their own information
        if hasattr(user, 'role') and user.role and user.role.role_name == 'citizen':
            return queryset.filter(email=user.email)
        return queryset

    def perform_create(self, serializer):
        instance = serializer.save()
        log_action(self.request.user, 'CREATE REQUESTER',
                   f'Added requester: {instance.agency_name}')

    def perform_update(self, serializer):
        instance = serializer.save()
        log_action(self.request.user, 'UPDATE REQUESTER',
                   f'Updated requester: {instance.agency_name}')

    def perform_destroy(self, instance):
        log_action(self.request.user, 'DELETE REQUESTER',
                   f'Deleted requester: {instance.agency_name}')
        instance.delete()


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [permissions.IsAuthenticated]


class PlatformViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    permission_classes = [permissions.IsAuthenticated]


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [IsOwnerOrStaff]

    def get_queryset(self):
        queryset = Request.objects.all().order_by('-submitted_at')
        user = self.request.user
        request_type = self.request.query_params.get('request_type')
        status = self.request.query_params.get('status')
        search = self.request.query_params.get('search')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')

        # Citizens only see their own requests
        if hasattr(user, 'role') and user.role and user.role.role_name == 'citizen':
            queryset = queryset.filter(requester__email=user.email)

        if request_type:
            queryset = queryset.filter(request_type=request_type)
        if status:
            queryset = queryset.filter(status__status_name=status)
        if search:
            queryset = queryset.filter(details__icontains=search)
        if date_from:
            queryset = queryset.filter(submitted_at__date__gte=date_from)
        if date_to:
            queryset = queryset.filter(submitted_at__date__lte=date_to)

        return queryset

    def perform_create(self, serializer):
        instance = serializer.save()
        log_action(self.request.user, 'CREATE REQUEST',
                   f'Submitted request #{instance.request_id}: {instance.get_request_type_display()}')
        send_notification(
            user=self.request.user,
            message=f'Your request #{instance.request_id} ({instance.get_request_type_display()}) has been successfully submitted and is now pending review.',
            notification_type='request_submitted'
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        log_action(self.request.user, 'UPDATE REQUEST',
                   f'Updated request #{instance.request_id}')
        send_notification(
            user=self.request.user,
            message=f'Your request #{instance.request_id} ({instance.get_request_type_display()}) has been updated.',
            notification_type='request_updated'
        )

    def perform_destroy(self, instance):
        log_action(self.request.user, 'DELETE REQUEST',
                   f'Deleted request #{instance.request_id}')
        instance.delete()

    @action(detail=False, methods=['get'], permission_classes=[IsStaffOrAdmin])
    def analytics(self, request):
        """
        Returns a breakdown of requests by Barangay.
        """
        stats = Request.objects.values('requester__barangay').annotate(
            total=Count('request_id')
        ).order_by('-total')

        # Format the data for the frontend
        formatted_stats = []
        # Create a dictionary of current choices for lookup
        choices_dict = dict(Requester._meta.get_field('barangay').choices)

        for entry in stats:
            b_code = entry['requester__barangay']
            formatted_stats.append({
                'barangay': choices_dict.get(b_code, b_code or 'Unknown'),
                'count': entry['total']
            })

        return Response(formatted_stats)


class ApprovalViewSet(viewsets.ModelViewSet):
    queryset = Approval.objects.all()
    serializer_class = ApprovalSerializer
    permission_classes = [IsStaffOrAdmin]

    def perform_create(self, serializer):
        instance = serializer.save(approved_by=self.request.user)
        log_action(self.request.user, 'CREATE APPROVAL',
                   f'Approval #{instance.approval_id}: {instance.approval_status}')

        # Find the citizen user who submitted the request (match by requester email)
        requester_email = instance.request.requester.email
        citizen = User.objects.filter(email=requester_email).first()

        if instance.approval_status == 'approved':
            message = (
                f'Good news! Your request #{instance.request.request_id} '
                f'({instance.request.get_request_type_display()}) '
                f'has been APPROVED.\n\nRemarks: {instance.remarks or "None"}'
            )
            notification_type = 'request_approved'
        elif instance.approval_status == 'rejected':
            message = (
                f'Your request #{instance.request.request_id} '
                f'({instance.request.get_request_type_display()}) '
                f'has been REJECTED.\n\nRemarks: {instance.remarks or "None"}'
            )
            notification_type = 'request_rejected'
        else:
            message = (
                f'Your request #{instance.request.request_id} '
                f'is now PENDING approval.'
            )
            notification_type = 'general'

        # Notify the citizen if found, otherwise notify the approver as fallback
        notify_user = citizen if citizen else self.request.user
        send_notification(
            user=notify_user,
            message=message,
            notification_type=notification_type
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        log_action(self.request.user, 'UPDATE APPROVAL',
                   f'Updated approval #{instance.approval_id}: {instance.approval_status}')


class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save(uploaded_by=self.request.user)
        log_action(self.request.user, 'UPLOAD ATTACHMENT',
                   f'Uploaded: {instance.file_name}')


class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save(published_by=self.request.user)
        log_action(self.request.user, 'CREATE PUBLICATION',
                   f'Published to {instance.platform}')


class ProcessingLogViewSet(viewsets.ModelViewSet):
    queryset = ProcessingLog.objects.all()
    serializer_class = ProcessingLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save(processed_by=self.request.user)
        log_action(self.request.user, 'PROCESSING LOG',
                   f'Step: {instance.process_step}')