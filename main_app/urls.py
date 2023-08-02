from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('workouts/', views.workouts_index, name='workouts_index'),
  path('exercises/', views.exercises_index, name='exercises_index'),
  path('accounts/signup/', views.signup, name='signup'),
]