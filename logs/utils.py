from .models import ActivityLog


def log_action(user, action, description=''):
    ActivityLog.objects.create(
        user=user,
        action=action,
        description=description
    )
