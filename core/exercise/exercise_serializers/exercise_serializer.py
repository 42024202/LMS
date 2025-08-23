from __future__ import annotations 
from rest_framework import serializers
from exercise.models.exercises import Exercise 


class ExerciseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ('lesson', 'title', 'description', 'status', 'due_at', 'max_score', 'sample_solution')

