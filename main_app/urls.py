from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('workouts_index/', views.workouts_index, name='workouts_index'),
  path('exercises/', views.exercises_index, name='exercises_index'),
  path('exercises/muscle/<str:muscle>/', views.muscle_index, name='muscle_index'),
  path('exercises_form/', views.exercises_form, name='exercises_form'),
  path('exercises<int:exercise_id>/', views.exercises_detail, name='detail'),
  path('exercises/<int:pk>/update/', views.ExerciseUpdate.as_view(), name='exercises_update'),
  path('exercises/<int:pk>/delete/', views.ExerciseDelete.as_view(), name='exercises_delete'),
  path('user_exercises/', views.user_exercises, name='user_exercises'),
  path('accounts/signup/', views.signup, name='signup'),
  path('profile/', views.profile, name='profile'),
  path('<int:pk>/update/', views.ProfileUpdate.as_view(), name='profiles_update'),
  path('<int:pk>/delete/', views.ProfileDelete.as_view(), name='profiles_delete'),
]