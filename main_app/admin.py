from django.contrib import admin
from .models import Exercise, Profile, ImportedExercise, ExerciseInWorkout, Workout
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class ExerciseResource(resources.ModelResource):
  class Meta:
    model = ImportedExercise

class ExerciseAdmin(ImportExportModelAdmin):
  resource_class = ExerciseResource


admin.site.register(ImportedExercise, ImportExportModelAdmin)
admin.site.register(Exercise)
admin.site.register(Profile)
admin.site.register(ExerciseInWorkout)
admin.site.register(Workout)
