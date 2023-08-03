from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Profile, Exercise
from .forms import ExerciseForm, ProfileForm
import requests
import json

# API-key = gXLCkA3vzl+aRqbGHmQJUg==isLFzMJoImFUhgL5
# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')


@login_required
def workouts_index(request):
  return render(request, 'workouts_index.html')

@login_required
def exercises_index(request):
  if request.method == 'GET':
    api_url = 'https://api.api-ninjas.com/v1/exercises?muscles='
    api_request = requests.get(api_url, headers={'X-Api-Key': 'gXLCkA3vzl+aRqbGHmQJUg==isLFzMJoImFUhgL5'})
    try:
      api = json.loads(api_request.content)
      # print(api_request.content)
    except Exception as e:
      api = "Opps, There was an error"
      print(e)
  return render(request, 'exercises/exercises_index.html', {'api': api})
  


  # muscle = 'biceps'
  # api_url = 'https://api.api-ninjas.com/v1/exercises?muscle={}'.format(muscle)
  # response = requests.get(api_url, headers={'X-Api-Key': 'gXLCkA3vzl+aRqbGHmQJUg==isLFzMJoImFUhgL5'})
  # if response.status_code == requests.codes.ok:
  #   print(response.text)
  # else:
  #   print("Error:", response.status_code, response.text)

@login_required
def profile(request):
  profile = Profile.objects.get(user=request.user)

  height_display = profile.height
  # if profile.height_unit == 'ft':
  #   height_display = profile.convert_height('ft')
  weight_display = profile.weight
  # if profile.weight_unit == 'lbs':
  #   weight_display = profile.convert_weight('lbs')

  context = {
    'profile': profile,
    'height_display': height_display,
    'weight_display': weight_display
  }
  return render(request, 'profile.html', context)

@login_required
def user_exercises(request):
    user_exercises = Exercise.objects.filter(user=request.user)
    return render(request, 'user_exercises.html', {'user_exercises': user_exercises})


@login_required
def exercises_form(request):
  if request.method == 'POST':
    form = ExerciseForm(request.POST)
    if form.is_valid():
      exercise = form.save(commit=False)
      exercise.user = request.user  # Set the user before saving
      exercise.save()
      # form.save()
      return redirect('exercises_index')
    else:
      return render(request, 'exercises_form.html', {'form': form})
  else:
      form = ExerciseForm()
  return render(request, 'exercises_form.html', {'form': form})




def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

class ProfileUpdate(UpdateView):
    model = Profile
    # form_class = ProfileForm
    fields = ['bio', 'age', 'height', 'height_unit', 'weight', 'weight_unit']
    # template_name = 'main_app/profile_form.html'
    # context_object_name = 'profile'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        profile = form.save(commit=False)

        # if 'height_unit' in form.changed_data:
        #     profile.height = profile.convert_height(profile.height_unit)
        # if 'weight_unit' in form.changed_data:
        #     profile.weight = profile.convert_weight(profile.weight_unit)

        profile.save()
        return super().form_valid(form)

class ProfileDelete(DeleteView):
    model = Profile
    success_url = '/'
