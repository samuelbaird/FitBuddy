from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('workouts_index/', views.workouts_index, name='workouts_index'),
  path('exercises_index/', views.exercises_index, name='exercises_index'),
  path('exercises_form/', views.exercises_form, name='exercises_form'),
  path('user_exercises/', views.user_exercises, name='user_exercises'),
  path('accounts/signup/', views.signup, name='signup'),
  path('profile/', views.profile, name='profile'),
  path('<int:pk>/update/', views.ProfileUpdate.as_view(), name='profiles_update'),
  path('<int:pk>/delete/', views.ProfileDelete.as_view(), name='profiles_delete'),
  path('workout/create/', views.create_workout, name='workout_create'),
  path('workouts/<int:pk>/update/', views.update_workout, name='workout_update'),
  path('workouts/<int:pk>/delete/', views.WorkoutDelete.as_view(), name='workout_delete'),
  path('workouts/<int:pk>/', views.workouts_detail, name='workouts_detail'),
  path('workouts/', views.workouts_index, name='workouts_index'),
]