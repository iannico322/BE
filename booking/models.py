from django.db import models

class Booking(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-generated ID field
    start_date = models.DateField(default=None, blank=True, null=True)
    end_date = models.DateField(default=None, blank=True, null=True)
    activity_title = models.CharField(max_length=255, blank=True)
    requestor_name = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
    contact_no = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    start_time = models.CharField(max_length=20)
    end_time = models.CharField(max_length=20)
    equipment = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=50, blank=True, default="pending")
    remarks = models.TextField(blank=True, null=True)
    attachment = models.CharField(max_length=1012, blank=True, null=True)  # Changed to string
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.activity_title} from {self.start_date} to {self.end_date}"