from django.db import models

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    amount = models.FloatField()
    duration_start = models.DateField()
    duration_end = models.DateField()
    about = models.TextField()
    employee = models.JSONField(default=list)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']