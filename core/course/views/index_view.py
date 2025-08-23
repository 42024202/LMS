from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from course.models.course import Course
from course.course_serializers.index_serializer import CourseModelSerializer as CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user
        if user.is_staff or user.is_superuser:
            role = "admin"
            courses = Course.objects.all()
        elif getattr(user, "role", None) == "instructor":
            role = "instructor"
            courses = Course.objects.filter(instructors__instructor=user)
        else:
            role = "student"
            courses = Course.objects.filter(students__student=user)
        serializer = self.get_serializer(courses, many=True)
        return Response({
            "role": role,
            "total_courses": courses.count(),
            "courses": serializer.data,
            "can_enroll": (role == "student" and courses.count() == 0)
        })

