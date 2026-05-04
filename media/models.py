from django.db import models


class FileType(models.Model):
    file_type_id = models.AutoField(primary_key=True)
    file_type_name = models.CharField(max_length=50)

    def __str__(self):
        return self.file_type_name


class MediaFile(models.Model):
    file_id = models.AutoField(primary_key=True)
    request = models.ForeignKey(
        'requests_app.Request',
        on_delete=models.CASCADE, related_name='media_files'
    )
    file_type = models.ForeignKey(
        FileType, on_delete=models.SET_NULL, null=True
    )
    file_name = models.CharField(max_length=255)
    file_path = models.FileField(upload_to='media_files/%Y/%m/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name
