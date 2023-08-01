from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('workouts/', views.workouts, name='workouts'),
  path('exercises/', views.exercises, name='exercises'),
  path('accounts/signup/', views.signup, name='signup'),
]