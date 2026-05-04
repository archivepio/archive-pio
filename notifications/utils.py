from django.core.mail import send_mail
from django.conf import settings
from .models import Notification


def send_notification(user, message, notification_type='general'):
    # Save to database
    notification = Notification.objects.create(
        user=user,
        message=message,
        notification_type=notification_type,
        email_sent=False
    )

    # Send email if user has email
    if user.email:
        try:
            send_mail(
                subject=f'ARCHIVE-PIO — {notification_type.replace("_", " ").title()}',
                message=f'''
Dear {user.name or user.username},

{message}

---
This is an automated message from ARCHIVE-PIO.
Public Information Office of Gumaca, Quezon.
Please do not reply to this email.
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            notification.email_sent = True
            notification.save()
        except Exception as e:
            print(f"Email failed: {e}")

    return notification