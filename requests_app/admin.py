from django.contrib import admin
from .models import (Requester, Status, Platform, Request,
                     Approval, Attachment, Publication, ProcessingLog)

admin.site.register(Requester)
admin.site.register(Status)
admin.site.register(Platform)
admin.site.register(Request)
admin.site.register(Approval)
admin.site.register(Attachment)
admin.site.register(Publication)
admin.site.register(ProcessingLog)
