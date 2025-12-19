from django.contrib import admin
from .models import Candidate

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'age', 'votes')
    search_fields = ('title', 'location')
    readonly_fields = ('votes', 'voters')
