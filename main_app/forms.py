from django import forms
from .models import Exercise, Profile

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = '__all__'
        exclude = ['user']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'age', 'height', 'height_unit', 'weight', 'weight_unit']
