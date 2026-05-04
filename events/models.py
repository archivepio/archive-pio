from django.db import models


class EventType(models.Model):
    event_type_id = models.AutoField(primary_key=True)
    event_type_name = models.CharField(max_length=100)

    def __str__(self):
        return self.event_type_name


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    request = models.ForeignKey(
        'requests_app.Request',
        on_delete=models.CASCADE, related_name='events'
    )
    event_type = models.ForeignKey(
        EventType, on_delete=models.SET_NULL, null=True
    )
    event_title = models.CharField(max_length=255)
    event_date = models.DateField()
    time_start = models.TimeField(null=True, blank=True)
    time_end = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.event_title
