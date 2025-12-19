from django.db import models

class QR(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255,blank=True)
    designation = models.CharField(max_length=255)
    lgu_agency = models.CharField(max_length=255, verbose_name="LGU/Agency")
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.lgu_agency}"

    class Meta:
        ordering = ['-created_date']
        verbose_name = "QR Code"
        verbose_name_plural = "QR Codes"