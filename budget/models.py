from django.db import models
from project.models import Project

class Budget(models.Model):
    id = models.AutoField(primary_key=True)
    proj_id = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        to_field='id',
        null=True,
        blank=True
    )
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.amount}"

    class Meta:
        ordering = ['-created_date']