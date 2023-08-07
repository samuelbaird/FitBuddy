from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver

WEIGHT = (
    ('kg', 'Kilograms'),
    ('lbs', 'Pounds'),
)

HEIGHT = (
    ('cm', 'Centimeters'),
    ('ft', 'Feet'),
)

DIFFICULTY = (
    ('b', 'Beginner'),
    ('i', 'Intermediate'),
    ('e', 'Expert'),
)

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    age = models.IntegerField(blank=True, null=True)
    
    height = models.IntegerField(blank=True, null=True)
    height_unit = models.CharField(
        max_length=100,
        blank=True,
        choices=HEIGHT,
        default=HEIGHT[0][0]
    )
    weight = models.IntegerField(blank=True, null=True)
    weight_unit = models.CharField(
        max_length=100,
        blank=True,
        choices=WEIGHT,
        default=WEIGHT[0][0]
    )

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('profile')
    
    def delete(self, *args, **kwargs):
        self.user.delete()
        super(Profile, self).delete(*args, **kwargs)

    # def convert_weight(self, target_unit):
    #     if self.weight_unit == target_unit:
    #         return self.weight

    #     if self.weight_unit == WeightUnitChoices.KG and target_unit == WeightUnitChoices.LBS:
    #         return self.weight * 2.20462
    #     elif self.weight_unit == WeightUnitChoices.LBS and target_unit == WeightUnitChoices.KG:
    #         return self.weight * 0.453592
    #     else:
    #         return self.weight

    # def convert_height(self, target_unit):
    #     if self.height_unit == target_unit:
    #         return self.height

    #     if self.height_unit == HeightUnitChoices.CM and target_unit == HeightUnitChoices.FT:
    #         feet = int(self.height / 30.48)
    #         inches = round((self.height % 30.48) / 2.54)
    #         return f"{feet} ft {inches} in"
    #     elif self.height_unit == HeightUnitChoices.FT and target_unit == HeightUnitChoices.CM:
    #         total_inches = self.height * 12
    #         return round(total_inches * 2.54)
    #     else:
    #         return self.height
        
@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
  
class ImportedExercise(models.Model):
    name = models.CharField(max_length=100, default='')
    force = models.CharField(max_length=100, default='', null=True, blank=True)
    level = models.CharField(
    max_length=20,
    choices=DIFFICULTY,
    default=DIFFICULTY[0][0],
    )
    mechanic = models.CharField(max_length=100, default='', null=True, blank=True)
    equipment = models.CharField(max_length=100, default='', null=True, blank=True)
    primaryMuscles = models.CharField(max_length=100, default='')
    secondaryMuscles = models.CharField(max_length=100, default='', null=True, blank=True)
    category = models.CharField(max_length=100, default='', null=True, blank=True)
    images = models.CharField(max_length=100, default='', null=True, blank=True)
    instructions = models.CharField(max_length=1000, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    imported = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} ({self.id})'

class Photo(models.Model):
    url = models.CharField(max_length=200)
    imported_exercise = models.ForeignKey(ImportedExercise, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for exercise_id: {self.imported_exercise_id} @{self.url}"

class Workout(models.Model):
  name = models.CharField(max_length=100)
  exercises = models.ManyToManyField('ImportedExercise', through='ExerciseInWorkout')
  is_template = models.BooleanField(default=True)
  date = models.DateField(null=True, blank=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE, default='1') 

  def __str__(self):
    return f'{self.name} ({self.id})'
  
  def get_absolute_url(self):
    return reverse('workouts_detail', kwargs={'pk': self.id})
  
  

class ExerciseInWorkout(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(ImportedExercise, on_delete=models.CASCADE)
    sets = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    reps = models.IntegerField(null=True, blank=True)
    tempo = models.CharField(max_length=10, null=True, blank=True)
    rest = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"{self.exercise} in {self.workout}"
