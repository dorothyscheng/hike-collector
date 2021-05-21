from django.db import models

# Create your models here.
class Hike(models.Model):
    name = models.CharField(max_length = 50)
    location = models.CharField(max_length = 50)
    state = models.CharField(max_length = 2)
    description = models.TextField()
    length = models.FloatField()
    elevation_gain = models.IntegerField()
    ROUTE_TYPE_CHOICES = (
        ('LP',  'Loop'),
        ('OB', 'Out & back'),
        ('PP', 'Point to point'),
    )
    route_type = models.CharField(max_length = 2, choices = ROUTE_TYPE_CHOICES)
    DIFFICULT_CHOICES = (
        ('E', 'Easy'),
        ('M', 'Moderate'),
        ('H', 'Hard'),
    )
