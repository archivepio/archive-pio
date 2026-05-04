from django.db import models
from django.conf import settings
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


BARANGAY_CHOICES = [
    ('adia_bitaog', 'Adia Bitaog'),
    ('anonangin', 'Anonangin'),
    ('bagong_buhay', 'Bagong Buhay (Poblacion)'),
    ('bamban', 'Bamban'),
    ('bantad', 'Bantad'),
    ('batong_dalig', 'Batong Dalig'),
    ('biga', 'Biga'),
    ('binambang', 'Binambang'),
    ('buensuceso', 'Buensuceso'),
    ('bungahan', 'Bungahan'),
    ('butaguin', 'Butaguin'),
    ('calumangin', 'Calumangin'),
    ('camohaguin', 'Camohaguin'),
    ('casasahan_ibaba', 'Casasahan Ibaba'),
    ('casasahan_ilaya', 'Casasahan Ilaya'),
    ('cawayan', 'Cawayan'),
    ('gayagayaan', 'Gayagayaan'),
    ('gitnang_barrio', 'Gitnang Barrio'),
    ('hagakhakin', 'Hagakhakin'),
    ('hardinan', 'Hardinan'),
    ('inaclagan', 'Inaclagan'),
    ('inagbuhan_ilaya', 'Inagbuhan Ilaya'),
    ('labnig', 'Labnig'),
    ('laguna', 'Laguna'),
    ('lagyo', 'Lagyo'),
    ('mabini', 'Mabini (Poblacion)'),
    ('mabunga', 'Mabunga'),
    ('malabtog', 'Malabtog'),
    ('manlayaan', 'Manlayaan'),
    ('marcelo_h_del_pilar', 'Marcelo H. del Pilar'),
    ('mataas_na_bundok', 'Mataas na Bundok'),
    ('maunlad', 'Maunlad (Poblacion)'),
    ('pagsabangan', 'Pagsabangan'),
    ('panikihan', 'Panikihan'),
    ('penafrancia', 'Peñafrancia (Poblacion)'),
    ('pipisik', 'Pipisik (Poblacion)'),
    ('progreso', 'Progreso'),
    ('rizal', 'Rizal (Poblacion)'),
    ('rosario', 'Rosario'),
    ('san_agustin', 'San Agustin'),
    ('san_diego_bukid', 'San Diego (Bukid)'),
    ('san_diego_poblacion', 'San Diego (Poblacion)'),
    ('san_isidro_kanluran', 'San Isidro Kanluran'),
    ('san_isidro_silangan', 'San Isidro Silangan'),
    ('san_juan_de_jesus', 'San Juan de Jesus'),
    ('san_vicente', 'San Vicente'),
    ('sastre', 'Sastre'),
    ('tabing_dagat', 'Tabing Dagat (Poblacion)'),
    ('tumayan', 'Tumayan'),
    ('villa_arcaya', 'Villa Arcaya'),
    ('villa_bota', 'Villa Bota'),
    ('villa_fuerte', 'Villa Fuerte'),
    ('villa_mendoza', 'Villa Mendoza'),
    ('villa_nava', 'Villa Nava'),
    ('villa_padua', 'Villa Padua'),
    ('villa_perez', 'Villa Perez'),
    ('villa_principe', 'Villa Principe'),
    ('villa_tanada', 'Villa Tañada'),
    ('villa_victoria', 'Villa Victoria'),
]


class Requester(models.Model):
    requester_id = models.AutoField(primary_key=True)
    agency_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=150)
    contact_number = models.CharField(max_length=30)
    email = models.EmailField()
    address = models.CharField(max_length=255, blank=True)
    barangay = models.CharField(
        max_length=100,
        choices=BARANGAY_CHOICES,
        null=True,
        blank=True
    )
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.latitude and not self.longitude:
            try:
                geolocator = Nominatim(user_agent="archive_pio")
                
                # Construct search string with address, barangay, and city for precision
                search_parts = []
                if self.address:
                    search_parts.append(self.address)
                if self.barangay:
                    search_parts.append(self.get_barangay_display())
                search_parts.append("Gumaca, Quezon, Philippines")
                
                search_query = ", ".join(search_parts)
                
                location = geolocator.geocode(search_query)
                if location:
                    self.latitude = location.latitude
                    self.longitude = location.longitude
            except (GeocoderTimedOut, Exception):
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return self.agency_name


class Status(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=50)

    def __str__(self):
        return self.status_name


class Platform(models.Model):
    platform_id = models.AutoField(primary_key=True)
    platform_name = models.CharField(max_length=100)

    def __str__(self):
        return self.platform_name


class Request(models.Model):
    REQUEST_TYPE_CHOICES = [
        ('social_media', 'Request for Social Media Announcements, Social Media Cards, Write Ups, and Communications'),
        ('image_editing', 'Request for Image Layout or Editing'),
        ('printed_media', 'Request for Printed Media (Image, Invitations, Certificate, ID Cards, Tarpaulin)'),
        ('photo_coverage', 'Request Photo Coverage for Documentation (Soft Copy)'),
        ('video_coverage', 'Request Video Coverage for Documentation (Soft Copy)'),
        ('video_editing', 'Request Video Editing'),
        ('radio_program', 'Request Radio Program Announcement and Guesting/Interviews'),
        ('live_streaming', 'Request for Live Video Streaming (Zoom, Youtube Live, Facebook Live)'),
        ('it_repair', 'Request for IT Equipment Repair/Maintenance'),
        ('leave_absence', 'Application for Leave of Absence'),
    ]

    request_id = models.AutoField(primary_key=True)
    requester = models.ForeignKey(
        Requester, on_delete=models.CASCADE, related_name='requests'
    )
    status = models.ForeignKey(
        Status, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='requests'
    )
    request_type = models.CharField(
        max_length=50,
        choices=REQUEST_TYPE_CHOICES,
        default='social_media'
    )
    details = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    result_link = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"Request #{self.request_id} - {self.get_request_type_display()}"


class Approval(models.Model):
    APPROVAL_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    approval_id = models.AutoField(primary_key=True)
    request = models.ForeignKey(
        Request, on_delete=models.CASCADE, related_name='approvals'
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True
    )
    approval_status = models.CharField(
        max_length=50,
        choices=APPROVAL_STATUS_CHOICES,
        default='pending'
    )
    remarks = models.TextField(blank=True)
    approved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Approval #{self.approval_id} - {self.approval_status}"


class Attachment(models.Model):
    attachment_id = models.AutoField(primary_key=True)
    request = models.ForeignKey(
        Request, on_delete=models.CASCADE, related_name='attachments'
    )
    file_name = models.CharField(max_length=255)
    file_path = models.FileField(upload_to='attachments/%Y/%m/')
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name


class Publication(models.Model):
    publication_id = models.AutoField(primary_key=True)
    request = models.ForeignKey(
        Request, on_delete=models.CASCADE, related_name='publications'
    )
    platform = models.ForeignKey(
        Platform, on_delete=models.SET_NULL, null=True
    )
    published_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True
    )
    post_link = models.URLField(blank=True)
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Publication #{self.publication_id}"


class ProcessingLog(models.Model):
    process_id = models.AutoField(primary_key=True)
    request = models.ForeignKey(
        Request, on_delete=models.CASCADE, related_name='processing_logs'
    )
    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True
    )
    action_taken = models.TextField()
    process_step = models.CharField(max_length=100)
    processed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Process #{self.process_id}"
