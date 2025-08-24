from __future__ import annotations
from rest_framework import serializers
from exercise.models.submission import Submission


class SubmissionModelSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()
    class Meta:
        model = Submission
        fields = ('exercise', 'student', 'attempt_no', 'content', 'status', 'created_at')

