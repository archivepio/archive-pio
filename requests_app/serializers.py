from rest_framework import serializers
from .models import (Requester, Status, Platform, Request,
                     Approval, Attachment, Publication, ProcessingLog)


class RequesterSerializer(serializers.ModelSerializer):
    barangay_display = serializers.CharField(
        source='get_barangay_display', read_only=True
    )

    class Meta:
        model = Requester
        fields = '__all__'


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = '__all__'


class RequestSerializer(serializers.ModelSerializer):
    request_type_display = serializers.CharField(
        source='get_request_type_display', read_only=True
    )

    class Meta:
        model = Request
        fields = '__all__'


class ApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Approval
        fields = '__all__'


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'


class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = '__all__'


class ProcessingLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessingLog
        fields = '__all__'
