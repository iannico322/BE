from django.db import models
from project.models import Project

class Expense(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    remarks = models.TextField(blank=True, null=True)
    proj_id = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        to_field='id',
        null=True,
        blank=True
    )
    date = models.DateField()
    amount = models.DecimalField(max_digits=65, decimal_places=2)  # Changed to max MySQL precision

    def __str__(self):
        return f"{self.item} - {self.amount}"

    class Meta:
        ordering = ['-date']