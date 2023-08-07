import uuid
import boto3
from django.http import HttpResponseBadRequest
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q
from .models import Profile, Workout, ExerciseInWorkout, ImportedExercise, DIFFICULTY
from .forms import ExerciseForm, ProfileForm, WorkoutForm
from collections import defaultdict
from datetime import date
import requests
import json

# API-key = gXLCkA3vzl+aRqbGHmQJUg==isLFzMJoImFUhgL5
# Create your views here.
def get_difficulty_label(key):
    for k, label in DIFFICULTY:
        if k == key:
            return label
    return ''


def home(request):
  if request.method == 'GET':
    api_url = 'https://api.api-ninjas.com/v1/quotes?category=dad'
    api_request = requests.get(api_url, headers={'X-Api-Key': 'gXLCkA3vzl+aRqbGHmQJUg==isLFzMJoImFUhgL5'})
    try:
      api_data = json.loads(api_request.content)
      if api_data and isinstance(api_data, list) and len(api_data) > 0:
        quote_info = api_data[0]
        quote = quote_info['quote']
        author = quote_info['author']
      else:
        quote = "No quotes available in the given category."
        author = "Unknown"

    except Exception as e:
      quote = "Oops, There was an error"
      author = "Unknown"
      print(e)

  return render(request, 'home.html', {'quote': quote, 'author': author})


def about(request):
  return render(request, 'about.html')

def map(request):
  return render(request, 'map.html')


@login_required
def exercises_index(request):
    all_exercises = ImportedExercise.objects.filter(Q(user=request.user) | Q(imported=True))

    categorized_exercises_dict = defaultdict(list)
    
    for exercise in all_exercises:
        primary_muscles = exercise.primaryMuscles
        categorized_exercises_dict[primary_muscles].append(exercise)

    categorized_exercises_dict = dict(categorized_exercises_dict)

    return render(request, 'exercises/exercises_index.html', {
        'combined_exercises_dict': categorized_exercises_dict,
    })

@login_required
def muscle_index(request, muscle):
    exercises = ImportedExercise.objects.filter(
        Q(primaryMuscles__contains=muscle) & 
        (Q(imported=True) | Q(user=request.user))
    )
    
    for exercise in exercises:
        if isinstance(exercise.images, str) and exercise.images:
            try:
                exercise.images = eval(exercise.images)
            except Exception as e:
                print(f"Failed to evaluate images for exercise {exercise.id}: {e}")
                exercise.images = []
        else:
            exercise.images = []
        
        exercise.name = exercise.name.replace('/', '-')
    
    context = {
        'muscle_name': muscle,
        'exercises': exercises,
    }
    return render(request, 'exercises/muscle_index.html', context)



def muscle_exercise_detail(request, muscle, exercise_id):
    exercise = ImportedExercise.objects.get(id=exercise_id)

    if isinstance(exercise.instructions, str) and exercise.instructions:
        try:
            exercise.instructions = eval(exercise.instructions)
        except SyntaxError:
            exercise.instructions = [exercise.instructions]
    else:
        exercise.instructions = []

    steps_list = []
    for instruction in exercise.instructions:
        steps = instruction.split('. ')
        steps_list.extend(steps)

    if isinstance(exercise.images, str) and exercise.images:
        try:
            exercise.images = eval(exercise.images)
        except Exception as e:
            print(f"Failed to evaluate images for exercise {exercise.id}: {e}")
            exercise.images = []
    else:
        exercise.images = []
        
    exercise_level_label = get_difficulty_label(exercise.level)

    context = {
        'muscle_name': muscle,
        'exercise': exercise,
        'steps_list': steps_list,
        'exercise_level_label': exercise_level_label,
    }
    return render(request, 'exercises/muscle_exercise_detail.html', context)



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
    user_exercises = ImportedExercise.objects.filter(user=request.user)

    for exercise in user_exercises:
        formatted_primary_muscles = [
            muscle.strip("[]'").capitalize() for muscle in exercise.primaryMuscles.split(',')
        ]
        exercise.primaryMuscles = ", ".join(formatted_primary_muscles)

        exercise.level = get_difficulty_label(exercise.level) 

    return render(request, 'exercises/user_exercises.html', {'user_exercises': user_exercises})

@login_required
def exercises_detail(request, exercise_id):
    exercise = get_object_or_404(ImportedExercise, id=exercise_id)


    formatted_primary_muscles = [
        muscle.strip("[]'").capitalize() for muscle in exercise.primaryMuscles.split(',')
    ]
    exercise.primaryMuscles = ", ".join(formatted_primary_muscles)

    exercise_level_label = get_difficulty_label(exercise.level)

    steps_list = []
    for instruction in exercise.instructions:
        steps = instruction.split('. ')
        steps_list.extend(steps)

    context = {
        'exercise': exercise,
        'exercise_level_label': exercise_level_label,
        'steps_list': steps_list,
    }
    return render(request, 'exercises/detail.html', context)


class ExerciseCreate(CreateView):
    model = ImportedExercise
    form_class = ExerciseForm
    template_name = 'main_app/exercises_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.imported = False

        photo_file = self.request.FILES.get('photo')
        if photo_file:
            unique_filename = f"{uuid.uuid4().hex}.jpg"

            s3_client = boto3.client('s3')
            s3_client.upload_fileobj(photo_file, 'fitbuddy-bucket', unique_filename)
            form.instance.photo = unique_filename
        else:
            form.instance.photo = None

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('detail', kwargs={'exercise_id': self.object.pk})
    
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

@login_required
def workouts_index (request):
    workouts = Workout.objects.filter(user=request.user, is_template=True)
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
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.is_template = True

            exercise_ids = request.POST.get('exercises').split(',')
            all_exercises_valid = True
            exercises_in_workout = []
            for exercise_id in exercise_ids:
              exercise_id = exercise_id.strip() 
              if exercise_id:
                exercise = ImportedExercise.objects.get(pk=int(exercise_id))
                exercise_in_workout = ExerciseInWorkout(workout=workout, exercise=exercise)
 
                sets = request.POST.get(f'sets_{exercise_id}')
                if sets and (not sets.isdigit() or int(sets) < 0):
                    all_exercises_valid = False
                    form.add_error(None, f'Invalid sets for exercise {exercise.name}')
                elif sets:
                    exercise_in_workout.sets = sets
                
                weight = request.POST.get(f'weight_{exercise_id}')
                if weight and (not weight.isdigit() or int(weight) < 0):
                    all_exercises_valid = False
                    form.add_error(None, f'Invalid weight for exercise {exercise.name}')
                elif weight:
                    exercise_in_workout.weight = weight

                reps = request.POST.get(f'reps_{exercise_id}')
                if reps and (not reps.isdigit() or int(reps) < 0):
                    all_exercises_valid = False
                    form.add_error(None, f'Invalid reps for exercise {exercise.name}')
                elif reps:
                    exercise_in_workout.reps = reps
                tempo = request.POST.get(f'tempo_{exercise_id}')
                if tempo and not re.match(r'^[\w-]+$', tempo):
                    all_exercises_valid = False
                    form.add_error(None, f'Invalid tempo for exercise {exercise.name}')
                elif tempo:
                    exercise_in_workout.tempo = tempo

                rest = request.POST.get(f'rest_{exercise_id}')
                if rest and not re.match(r'^[\w-]+$', rest):
                    all_exercises_valid = False
                    form.add_error(None, f'Invalid rest for exercise {exercise.name}')
                elif rest:
                    exercise_in_workout.rest = rest
                
                if all_exercises_valid:
                    exercises_in_workout.append(exercise_in_workout)

            if all_exercises_valid:
                workout.user = request.user
                workout.save()
                for exercise_in_workout in exercises_in_workout:
                    exercise_in_workout.save()

                return redirect('workouts_detail', pk=workout.pk)
            else:
                messages.error(request, 'Some fields are not valid. Please check your entries.')
        else:
            print('form is not valid')
            print(form.errors)

    form = WorkoutForm()
    exercise_list = ImportedExercise.objects.filter(Q(user=request.user) | Q(imported=True))
    return render(request, 'workouts/workout_form.html', {'form': form, 'exercise_list': exercise_list})

def update_workout(request, pk):
    workout = get_object_or_404(Workout, pk=pk)

    if request.method == 'POST':
        form = WorkoutForm(request.POST, instance=workout)
        print(request.POST)
        if form.is_valid():
            workout.is_template = True
            print('form is valid')
            form.save()

            exercise_ids = request.POST.get('exercises').split(',')

            exercises_in_workout = {e.exercise.id: e for e in ExerciseInWorkout.objects.filter(workout=workout)}

            all_exercises_valid = True

            for exercise_id in exercise_ids:
                exercise_id = exercise_id.strip()
                if exercise_id:
                    exercise = ImportedExercise.objects.get(pk=int(exercise_id))

                    if exercise.id in exercises_in_workout:
                        exercise_in_workout = exercises_in_workout.pop(exercise.id)
                    else:
                        exercise_in_workout = ExerciseInWorkout(workout=workout, exercise=exercise)

                    sets = request.POST.get(f'sets_{exercise_id}')
                    if sets and (not sets.isdigit() or int(sets) < 0):
                        all_exercises_valid = False
                        form.add_error(None, f'Invalid sets for exercise {exercise.name}')
                    elif sets:
                        exercise_in_workout.sets = sets

                    weight = request.POST.get(f'weight_{exercise_id}')
                    if weight and (not weight.isdigit() or int(weight) < 0):
                        all_exercises_valid = False
                        form.add_error(None, f'Invalid weight for exercise {exercise.name}')
                    elif weight:
                        exercise_in_workout.weight = weight

                    reps = request.POST.get(f'reps_{exercise_id}')
                    if reps and (not reps.isdigit() or int(reps) < 0):
                        all_exercises_valid = False
                        form.add_error(None, f'Invalid reps for exercise {exercise.name}')
                    elif reps:
                        exercise_in_workout.reps = reps

                    tempo = request.POST.get(f'tempo_{exercise_id}')
                    if tempo and not re.match(r'^[\w-]+$', tempo):
                        all_exercises_valid = False
                        form.add_error(None, f'Invalid tempo for exercise {exercise.name}')
                    elif tempo:
                        exercise_in_workout.tempo = tempo

                    rest = request.POST.get(f'rest_{exercise_id}')
                    if rest and not re.match(r'^[\w-]+$', rest):
                        all_exercises_valid = False
                        form.add_error(None, f'Invalid rest for exercise {exercise.name}')
                    elif rest:
                        exercise_in_workout.rest = rest

                    if all_exercises_valid:
                        exercise_in_workout.save()

            for remaining in exercises_in_workout.values():
                remaining.delete()

            if all_exercises_valid:
                return redirect('workouts_detail', pk=workout.pk)
            else:
                messages.error(request, 'Some fields are not valid. Please check your entries.')
    else:
        form = WorkoutForm(instance=workout)
        if not form.is_valid():
            print('form is not valid')

    exercise_list = ImportedExercise.objects.filter(Q(user=request.user) | Q(imported=True))
    return render(request, 'workouts/workout_form.html', {
        'form': form,
        'exercise_list': exercise_list,
        'workout_name': workout.name,
    })

class ExerciseUpdate(UpdateView):
    model = ImportedExercise
    form_class = ExerciseForm
    template_name = 'main_app/exercises_form.html'

    def get_object(self, queryset=None):
        obj = super().get_object()
        if not obj.user == self.request.user:
            raise HttpResponseForbidden("You are not allowed to edit this exercise.")
        return obj

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ExerciseDelete(DeleteView):
    model = ImportedExercise
    success_url = '/'  

    def get_object(self, queryset=None):
        obj = super().get_object()
        if not obj.user == self.request.user:
            raise HttpResponseForbidden("You are not allowed to delete this exercise.")
        return obj


def begin_workout(request, pk):
    template_workout = get_object_or_404(Workout, pk=pk)
    form = WorkoutForm(instance=template_workout)
    if request.method == 'POST':
        new_workout = Workout.objects.create(
            name=template_workout.name,
            user=template_workout.user,
            is_template=False,
            date=date.today()
        )
        for e in template_workout.exerciseinworkout_set.all():
            sets = request.POST.get(f'sets_{e.id}')
            weight = request.POST.get(f'weight_{e.id}')
            reps = request.POST.get(f'reps_{e.id}')
            tempo = request.POST.get(f'tempo_{e.id}')
            rest = request.POST.get(f'rest_{e.id}')

            ExerciseInWorkout.objects.create(
                workout=new_workout,
                exercise=e.exercise,
                sets=sets,
                weight=weight,
                reps=reps,
                tempo=tempo,
                rest=rest
            )

        return redirect(new_workout.get_absolute_url())

    else:
        exercise_in_workouts = ExerciseInWorkout.objects.filter(workout=template_workout)
        return render(request, 'workouts/begin_workout.html', {
            'workout': template_workout,
            'exercise_in_workouts': exercise_in_workouts,
            'form': form
        })

@login_required
def workouts_history(request):
    workouts = Workout.objects.filter(user=request.user, is_template=False).order_by('-date')
    return render(request, 'workouts/history.html', {
        'workouts': workouts
    })