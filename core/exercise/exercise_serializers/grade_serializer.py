from __future__ import annotations
from rest_framework import serializers
from exercise.models.grade import Grade


class GradeModelSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()
    class Meta:
        model = Grade
        fields = ('submission', 'score', 'student', 'feedback', 'grade_at')

