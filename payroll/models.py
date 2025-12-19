from django.db import models
from project.models import Project

class Payroll(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    date_start = models.DateField()
    date_end = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.project}"

    class Meta:
        ordering = ['-date_start']