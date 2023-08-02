from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Profile
from .forms import ExerciseForm
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
  return render(request, 'profile.html', {'profile': profile})

@login_required
def exercises_form(request):
  if request.method == 'POST':
    form = ExerciseForm(request.POST)
    if form.is_valid():
      form.save()
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
    fields = ['bio', 'age', 'height', 'weight']

class ProfileDelete(DeleteView):
    model = Profile
    success_url = '/'
