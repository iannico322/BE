from django.db import models

# Create your models here.

class Performer(models.Model):
    name = models.CharField(max_length=255, help_text="Name of the performer")
    photo = models.ImageField(upload_to='performers/', null=True, blank=True, help_text="Photo of the performer (optional)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class JudgingCriteria(models.Model):
    performer = models.ForeignKey(Performer, on_delete=models.CASCADE, related_name='ratings')
    rater = models.CharField(max_length=255, help_text="Name of the rater")
    # ratings format: [talent, creativity, stage_presence, relevance_of_ict, time_adherence]
    ratings = models.JSONField(default=list, help_text="List of scores [Talent, Creativity, Stage Presence, Relevance of ICT, Time Adherence]")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('performer', 'rater')
    
    def __str__(self):
        return f"{self.rater} rated {self.performer.name}"
    
    @property
    def total_score(self):
        return sum(self.ratings) if self.ratings else 0
