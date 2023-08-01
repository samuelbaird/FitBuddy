from django.shortcuts import render

# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def workouts(request):
  return render(request, 'workouts.html')

def exercises(request):
  return render(request, 'exercises.html')
