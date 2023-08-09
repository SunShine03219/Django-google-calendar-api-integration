
# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from Project.models import Project

class Meetings(models.Model):
    
    #project = models.ForeignKey(Project, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=200)
    google_meet = models.CharField(max_length=200)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title