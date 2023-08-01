from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('workouts_index/', views.workouts_index, name='workouts_index'),
  path('exercises_index/', views.exercises_index, name='exercises_index'),
  path('exercises_form/', views.exercises_form, name='exercises_form'),
  path('accounts/signup/', views.signup, name='signup'),
]