from django.db import models

class Template(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    body = models.JSONField(default=dict, blank=True)
    file = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name