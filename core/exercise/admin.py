from django.contrib import admin
from .models.exercises import Exercise
from .models.grade import Grade
from .models.submission import Submission


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['attempt_no', 'exercise', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['content']
    

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['score', 'submission', 'grade_at']
    list_filter = ['score']
    search_fields = ['score', 'feedback']


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'status']
    list_filter = ['status']
    search_fields = ['title', 'description', 'status']

