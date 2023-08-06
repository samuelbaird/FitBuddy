from django import forms
from django.forms import ModelForm
from .models import Exercise, Profile, Workout, DIFFICULTY

class ExerciseForm(forms.ModelForm):
    level = forms.ChoiceField(choices=DIFFICULTY)
    class Meta:
        model = Exercise
        fields = ['name', 'level', 'primaryMuscles', 'images', 'instructions']
        exclude = ['user']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'age', 'height', 'height_unit', 'weight', 'weight_unit']

class WorkoutForm(ModelForm):
    class Meta:
        model = Workout
        fields = ['name', 'date', 'exercises', 'is_template']
