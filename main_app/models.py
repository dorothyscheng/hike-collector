from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Create your models here.
class Hike(models.Model):
    name = models.CharField(max_length = 50, unique=True)
    location = models.CharField(max_length = 50)
    state = models.CharField(max_length = 2)
    description = models.TextField()
    length = models.FloatField()
    elevation_gain = models.IntegerField()
    average_rating = models.IntegerField(null=True)
    ROUTE_TYPE_CHOICES = (
        ('LP',  'Loop'),
        ('OB', 'Out & back'),
        ('PP', 'Point to point'),
    )
    route_type = models.CharField(max_length = 2, choices = ROUTE_TYPE_CHOICES)
    DIFFICULTY_CHOICES = (
        ('E', 'Easy'),
        ('M', 'Moderate'),
        ('H', 'Hard'),
    )
    difficulty = models.CharField(max_length=1, choices=DIFFICULTY_CHOICES)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('hikes:detail', kwargs={'hike_id': self.pk})

class Photo(models.Model):
    url = models.CharField(max_length=500)
    hike = models.ForeignKey(Hike, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'Photo for {self.hike} by {self.user}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorites = models.ManyToManyField(Hike, related_name='favorite', blank=True)
    completed = models.ManyToManyField(Hike, related_name='completed', blank=True)

# reference: https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hike = models.ForeignKey(Hike, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField()
    def __str__(self):
        return f'Review for {self.hike} by {self.user}'

def calculate_average_rating(hike):
    all_hike_reviews = Review.objects.filter(hike=hike)
    if len(all_hike_reviews) == 0:
        return None
    else:
        rating_sum  = 0
        for review in all_hike_reviews:
            rating_sum += review.rating
        return rating_sum // len(all_hike_reviews)

@receiver(post_delete, sender=Review)
def update_rating_on_delete(sender, instance, **kwargs):
    instance.hike.average_rating = calculate_average_rating(instance.hike)
    instance.hike.save()