from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Count
from django.db.models.functions import TruncMonth
from requests_app.models import Request, Requester
from logs.models import ActivityLog
from users.models import User


class DashboardStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        total_requests = Request.objects.count()
        total_requesters = Requester.objects.count()
        total_users = User.objects.count()

        status_breakdown = Request.objects.values(
            'status__status_name'
        ).annotate(count=Count('request_id'))

        monthly_trend = Request.objects.annotate(
            month=TruncMonth('submitted_at')
        ).values('month').annotate(
            count=Count('request_id')
        ).order_by('month')

        top_requesters = Requester.objects.annotate(
            request_count=Count('requests')
        ).order_by('-request_count')[:5].values(
            'agency_name', 'request_count'
        )

        recent_activities = ActivityLog.objects.all()[:10].values(
            'action', 'description', 'created_at', 'user__username'
        )

        geo_data = Requester.objects.exclude(
            latitude=None
        ).exclude(
            longitude=None
        ).values(
            'agency_name', 'address', 'latitude', 'longitude'
        )

        request_type_breakdown = Request.objects.values(
            'request_type'
        ).annotate(count=Count('request_id')).order_by('-count')

        return Response({
            'total_requests': total_requests,
            'total_requesters': total_requesters,
            'total_users': total_users,
            'status_breakdown': list(status_breakdown),
            'monthly_trend': list(monthly_trend),
            'top_requesters': list(top_requesters),
            'recent_activities': list(recent_activities),
            'geo_data': list(geo_data),
            'request_type_breakdown': list(request_type_breakdown),
        })
