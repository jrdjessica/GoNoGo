from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    content = models.CharField(max_length=500)
    location = models.CharField(max_length=50)
    date = models.DateField()
    
    time = models.TimeField()
    decision = models.BooleanField()
    attendees = models.ManyToManyField(User)
    organizer = models.ForeignKey(User, related_name='events_organizing', on_delete=models.SET_NULL, null=True) 
    
    


    def __str__(self):
        return f"{self.title}"
class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    individual_decision = models.BooleanField()

    class Meta:
        unique_together = ['user', 'event']
