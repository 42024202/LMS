from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from course.models.course import Course
from exercise.models.grade import Grade
from exercise.exercise_serializers.grade_serializer import GradeModelSerializer


class StudentCourseGradesViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    Возвращает все оценки текущего пользователя в рамках конкретного курса.
    """
    serializer_class = GradeModelSerializer

    def get_queryset(self):
        course_id = self.kwargs.get("course_pk")  # <-- NestedSimpleRouter передаёт course_pk
        course = get_object_or_404(Course, id=course_id)

        return Grade.objects.filter(
            submission__student=self.request.user,
            submission__exercise__lesson__module__course=course
        ).select_related("submission", "submission__exercise")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        course_id = self.kwargs.get("course_pk")
        course = get_object_or_404(Course, id=course_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "course_id": course.id,
            "course_title": course.title,
            "total_grades": queryset.count(),
            "grades": serializer.data
        })

