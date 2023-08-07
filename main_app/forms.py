
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
        fields = ['name', 'level', 'primaryMuscles', 'images', 'instructions', 'photo']

# class ExerciseForm(forms.ModelForm):
#     level = forms.ChoiceField(choices=DIFFICULTY)
#     primaryMuscles = forms.ChoiceField()

#     class Meta:
#         model = Exercise
#         fields = ['name', 'level', 'primaryMuscles', 'images', 'instructions']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['primaryMuscles'].choices = self.get_unique_primary_muscles()

#     def get_unique_primary_muscles(self):
#         unique_primary_muscles = set()
#         for exercise in ImportedExercise.objects.all():
#             primary_muscles = exercise.primaryMuscles.strip("[]'").split(',')
#             for muscle in primary_muscles:
#                 unique_primary_muscles.add(muscle.strip())
#         return [(muscle, muscle) for muscle in unique_primary_muscles]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'age', 'height', 'height_unit', 'weight', 'weight_unit']

class WorkoutForm(ModelForm):
    class Meta:
        model = Workout
        fields = ['name', 'date', 'exercises', 'is_template']
