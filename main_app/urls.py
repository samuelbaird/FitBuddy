from django.urls import path
from . import views

urlpatterns = [
  path('home/', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('workouts_index/', views.workouts_index, name='workouts_index'),
  path('exercises_index/', views.exercises_index, name='exercises_index'),
  path('exercises_form/', views.exercises_form, name='exercises_form'),
  path('user_exercises/', views.user_exercises, name='user_exercises'),
  path('accounts/signup/', views.signup, name='signup'),
  path('profile/', views.profile, name='profile'),
  path('<int:pk>/update/', views.ProfileUpdate.as_view(), name='profiles_update'),
  path('<int:pk>/delete/', views.ProfileDelete.as_view(), name='profiles_delete'),
]