from django import forms
from django.forms import ModelForm
from .models import Exercise, Profile, Workout

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = '__all__'
        exclude = ['user']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'age', 'height', 'height_unit', 'weight', 'weight_unit']

class WorkoutForm(ModelForm):
    class Meta:
        model = Workout
        fields = ['name', 'date', 'exercises', 'is_template']
