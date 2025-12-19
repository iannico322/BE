from django.db import models

# Create your models here.

class Candidate(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    title = models.CharField(max_length=255, help_text="Name of the candidate")
    location = models.CharField(max_length=255, help_text="Location of the candidate")
    age = models.IntegerField(help_text="Age of the candidate")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,default='M', help_text="Gender of the candidate")
    image = models.ImageField(upload_to='candidates/', help_text="Image for the candidate")
    votes = models.IntegerField(default=0, help_text="Number of votes received by the candidate")
    voters = models.JSONField(default=list, help_text="List of voter names who voted for this candidate")
    

    def __str__(self):
        return self.title
