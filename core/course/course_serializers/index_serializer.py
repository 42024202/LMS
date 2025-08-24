from rest_framework import serializers 
from course.models.course import Course


class CourseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'title', 'price', 'starts_at', 'end_at', 'description', 'is_active', 'duration')

