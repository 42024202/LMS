from __future__ import annotations
from rest_framework import serializers
from course.models.lessons import Lesson


class LessonModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('title', 'description', 'content', 'position', 'starts_at', 'end_at', 'meeting_url')

