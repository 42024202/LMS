from course.models.course import Course 
from course.models.attendance import Attendance
from course.models.shedule_session import SheduleSession
from course.course_serializers.attendance_serializer import AttendanceModelSerializer, SheduleSessionModelSerializer
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from common.permissions import IsInstructorOrAdmin
from course.models.course_student import CourseStudent



class StudentCourseAttendanceViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Получить посещаемость студентов в рамках курса.
    - Студент видит только свои посещения.
    - Преподаватель/админ видят всех студентов (можно фильтровать по student_id).
    """
    serializer_class = AttendanceModelSerializer
    permission_classes = [IsInstructorOrAdmin]

    def get_queryset(self):
        course_id = self.kwargs.get("course_pk")
        course = get_object_or_404(Course, id=course_id)

        user = self.request.user

        qs = Attendance.objects.filter(shedule_session__course=course).select_related(
            "student",
            "student__user",         
            "shedule_session",       
            "shedule_session__course",
            "shedule_session__lesson" 
            )

        # если студент — показываем только его посещения
        if not (user.is_staff or user.is_superuser):
            try:
                course_student = CourseStudent.objects.get(course=course, user=user)
                qs = qs.filter(student=course_student)
            except CourseStudent.DoesNotExist:
                qs = qs.none()
        else:
            student_id = self.request.query_params.get("student_id")
            if student_id:
                qs = qs.filter(student_id=student_id)

        return qs

