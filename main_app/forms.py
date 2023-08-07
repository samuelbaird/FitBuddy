
from django import forms
from django.forms import ModelForm
from .models import ImportedExercise, Profile, Workout, DIFFICULTY

class ExerciseForm(forms.ModelForm):
    level = forms.ChoiceField(
        choices=DIFFICULTY,
        widget=forms.Select(attrs={'class':'browser-default'}),
    )
    primaryMuscles = forms.ChoiceField(
        choices=[(muscle, muscle) for muscle in set(ImportedExercise.objects.values_list('primaryMuscles', flat=True).distinct())],
        widget=forms.Select(attrs={'class':'browser-default'}),
    )

    class Meta:
        model = ImportedExercise
        fields = ['name', 'level', 'primaryMuscles', 'instructions', 'photo']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'age', 'height', 'height_unit', 'weight', 'weight_unit']

class WorkoutForm(ModelForm):
    class Meta:
        model = Workout
        fields = ['name', 'date', 'exercises', 'is_template']
