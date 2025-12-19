from django.db import models
from accounts.models import UserAccount
from template.models import Template

def generate_tracking_id(instance):
    import datetime
    unique_number = instance.pk if instance.pk else 'NEW'
    created_date = datetime.datetime.now().strftime('%Y%m%d')
    return f"D-{unique_number}-{created_date}-R10"

class Document(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    status = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        UserAccount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='documents_created'
    )
    submitted_by = models.CharField(max_length=255, blank=True, null=True)
    template = models.ForeignKey(
        Template,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='documents'
    )
    document_data = models.JSONField(default=dict, blank=True)
    to_route = models.IntegerField( blank=True, null=True)
    assignatures = models.JSONField(default=dict, blank=True)
    remarks = models.JSONField(default=dict, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    tracking_id = models.CharField(max_length=255, unique=True, blank=True)
    isupload = models.BooleanField(default=False, blank=True)
    uploadedFile = models.FileField(upload_to='documents/', null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.tracking_id:
            super().save(*args, **kwargs)  # Save to get pk
            self.tracking_id = f"D-{self.pk}-{self.date_created.strftime('%Y%m%d')}-R10"
            # Save again to persist tracking_id
            super().save(update_fields=['tracking_id'])
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.tracking_id})"