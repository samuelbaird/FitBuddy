from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Profile, Exercise, Workout, ExerciseInWorkout, ImportedExercise
from .forms import ExerciseForm, ProfileForm, WorkoutForm
from collections import defaultdict
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
  all_exercises = ImportedExercise.objects.all()
  categorized_exercises_dict = defaultdict(list)

  for exercise in all_exercises:
      primary_muscles = exercise.primaryMuscles
      categorized_exercises_dict[primary_muscles].append(exercise)

  categorized_exercises_dict = dict(categorized_exercises_dict)


  return render(request, 'exercises/exercises_index.html', {
    'categorized_exercises_dict': categorized_exercises_dict
  })
  # if request.method == 'GET':
  #   api_url = 'https://api.api-ninjas.com/v1/exercises?muscles='
  #   api_request = requests.get(api_url, headers={'X-Api-Key': 'gXLCkA3vzl+aRqbGHmQJUg==isLFzMJoImFUhgL5'})
  #   try:
  #     api = json.loads(api_request.content)
  #     # print(api_request.content)
  #   except Exception as e:
  #     api = "Opps, There was an error"
  #     print(e)

@login_required
def muscle_index(request, muscle):
  exercises = ImportedExercise.objects.filter(primaryMuscles__contains=muscle)
  context = {
      'muscle_name': muscle,
      'exercises': exercises,
  }
  return render(request, 'exercises/muscle_index.html', context)

def muscle_exercise_detail(request, muscle, exercise_id):
  exercise = ImportedExercise.objects.get(id=exercise_id)
  text_array = exercise.instructions.split('\n')

  all_text = ' '.join(text_array)
  separated_items = all_text.split('. ')
  separated_items = [item.strip() for item in separated_items]
  context = {
      'muscle_name': muscle,
      'exercise': exercise,
      'separated_items': separated_items,
  }
  return render(request, 'exercises/muscle_exercise_detail.html', context)

@login_required
def exercises_detail(request, exercise_id):
  exercise = Exercise.objects.get(id=exercise_id)
  return render(request, 'exercises/detail.html', {
    'exercise': exercise
  })

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
      return redirect('user_exercises')
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


class WorkoutDelete(DeleteView):
    model = Workout
    success_url = '/workouts/'

def workouts_index (request):
    workouts = Workout.objects.all()
    return render(request, 'workouts/index.html', {
        'workouts': workouts
    })

def workouts_detail(request, pk):
    workout = Workout.objects.get(id=pk)
    exercise_in_workouts = ExerciseInWorkout.objects.filter(workout=workout)
    return render(request, 'workouts/detail.html', {
        'workout': workout,
        'exercise_in_workouts': exercise_in_workouts,
    })

def create_workout(request):
    if request.method == 'POST':
        print(request.POST)
        form = WorkoutForm(request.POST)
        if form.is_valid():
            print('form is valid')
            workout = form.save()

            exercise_ids = request.POST.getlist('exercises')  

            for exercise_id in exercise_ids:
                exercise = ImportedExercise.objects.get(pk=int(exercise_id))
                exercise_in_workout = ExerciseInWorkout(workout=workout, exercise=exercise)
 
                exercise_in_workout.sets = request.POST.get(f'sets_{exercise_id}')
                exercise_in_workout.weight = request.POST.get(f'weight_{exercise_id}')
                exercise_in_workout.reps = request.POST.get(f'reps_{exercise_id}')
                exercise_in_workout.tempo = request.POST.get(f'tempo_{exercise_id}')
                exercise_in_workout.rest = request.POST.get(f'rest_{exercise_id}')
                exercise_in_workout.save()

            return redirect('workouts_detail', pk=workout.pk)
    else:
        print('form is not valid')
        form = WorkoutForm()

    exercise_list = ImportedExercise.objects.all()
    return render(request, 'workouts/workout_form.html', {'form': form, 'exercise_list': exercise_list})

def update_workout(request, pk):
    workout = get_object_or_404(Workout, pk=pk)

    if request.method == 'POST':
        form = WorkoutForm(request.POST, instance=workout)
        if form.is_valid():
            form.save()


            exercise_ids = request.POST.getlist('exercises')  


            ExerciseInWorkout.objects.filter(workout=workout).delete()


            for exercise_id in exercise_ids:
                exercise = ImportedExercise.objects.get(pk=int(exercise_id))
                exercise_in_workout = ExerciseInWorkout(workout=workout, exercise=exercise)
 
                exercise_in_workout.sets = request.POST.get(f'sets_{exercise_id}')
                exercise_in_workout.weight = request.POST.get(f'weight_{exercise_id}')
                exercise_in_workout.reps = request.POST.get(f'reps_{exercise_id}')
                exercise_in_workout.tempo = request.POST.get(f'tempo_{exercise_id}')
                exercise_in_workout.rest = request.POST.get(f'rest_{exercise_id}')
                exercise_in_workout.save()

            return redirect('workouts_detail', pk=workout.pk)
    else:
        form = WorkoutForm(instance=workout)

    exercise_list = ImportedExercise.objects.all()
    return render(request, 'workouts/workout_form.html', {
        'form': form,
        'exercise_list': exercise_list,
        'workout_name': workout.name,  
    })

class ExerciseUpdate(UpdateView):
  model = Exercise
  fields = '__all__'

class ExerciseDelete(DeleteView):
  model = Exercise
  success_url = '/'  

