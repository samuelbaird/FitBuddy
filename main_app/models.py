from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    age = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)


    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('profile')
    
    def delete(self, *args, **kwargs):
        self.user.delete()
        super(Profile, self).delete(*args, **kwargs)
        
@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
  

class Exercise(models.Model):
     name = models.CharField(max_length=100, default='')
     force = models.CharField(max_length=100, default='')
     level = models.CharField(max_length=100, default='')
     mechanic = models.CharField(max_length=100, default='')
     equipment = models.CharField(max_length=100, default='')
     primaryMuscles = models.CharField(max_length=100, default='')
     secondaryMuscles = models.CharField(max_length=100, default='')
     category = models.CharField(max_length=100, default='')
     images = models.CharField(max_length=100, default='')
     instructions = models.CharField(max_length=200, default='')

     user = models.ForeignKey(User, on_delete=models.CASCADE)

     def __str__(self):
        return f'{self.name} ({self.id})'

     def get_absolute_url(self):
        return reverse('detail', kwargs={'exercise_id': self.id})
