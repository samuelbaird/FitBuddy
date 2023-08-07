from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('map/', views.map, name='map'),
  path('workouts_index/', views.workouts_index, name='workouts_index'),
  path('exercises/', views.exercises_index, name='exercises_index'),
  path('exercises/create/', views.ExerciseCreate.as_view(), name='exercises_form'),
  path('exercises/<str:muscle>/', views.muscle_index, name='muscle_exercise_index'),
  path('exercises/<str:muscle>/<int:exercise_id>/', views.muscle_exercise_detail, name='muscle_exercise_detail'),
  path('exercises<int:exercise_id>/', views.exercises_detail, name='detail'),
  path('exercises/<int:pk>/update/', views.ExerciseUpdate.as_view(), name='exercises_update'),
  path('exercises/<int:pk>/delete/', views.ExerciseDelete.as_view(), name='exercises_delete'),
  path('user_exercises/', views.user_exercises, name='user_exercises'),
  path('accounts/signup/', views.signup, name='signup'),
  path('profile/', views.profile, name='profile'),
  path('<int:pk>/update/', views.ProfileUpdate.as_view(), name='profiles_update'),
  path('<int:pk>/delete/', views.ProfileDelete.as_view(), name='profiles_delete'),
  path('workout/create/', views.create_workout, name='workout_create'),
  path('workouts/<int:pk>/begin/', views.begin_workout, name='begin_workout'),
  path('workouts/<int:pk>/update/', views.update_workout, name='workout_update'),
  path('workouts/<int:pk>/delete/', views.WorkoutDelete.as_view(), name='workout_delete'),
  path('workouts/<int:pk>/', views.workouts_detail, name='workouts_detail'),
  path('workouts/', views.workouts_index, name='workouts_index'),
  path('workouts/history', views.workouts_history, name='workouts_history'),
]