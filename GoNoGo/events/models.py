from django.db import models
# from ..authentication.models import User
class Event(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    content = models.CharField(max_length=500)
    location = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField()
    decision = models.BooleanField()
    attendees = models.ManyToManyField('authentication.User')
    organizer = models.ForeignKey('authentication.User', related_name='events_organizing', on_delete=models.SET_NULL, null=True) 
    
    


    def __str__(self):
        return f"{self.title}"
