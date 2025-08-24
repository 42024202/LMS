from rest_framework import viewsets, permissions
from common.permissions import IsInstructorOrAdmin
from rest_framework.response import Response
from course.models.course import Course
from course.models.modules import Module
from course.models.lessons import Lesson
from course.course_serializers.index_serializer import CourseModelSerializer as CourseSerializer
from course.course_serializers.modules_serializer import ModuleModelSerializer
from course.course_serializers.lessons_serializer import LessonModelSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsInstructorOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Course.objects.all()
        elif user.is_staff or getattr(user, "role", None) == "instructor":
            return Course.objects.filter(instructors__instructor=user)
        return Course.objects.filter(students__user=user)

    def list(self, request, *args, **kwargs):
        courses = self.get_queryset()
        user = request.user

        if user.is_superuser:
            role = "admin"
        elif user.is_staff or getattr(user, "role", None) == "instructor":
            role = "instructor"
        else:
            role = "student"

        serializer = self.get_serializer(courses, many=True)

        return Response({
            "role": role,
            "total_courses": courses.count(),
            "can_edit": role in ("admin", "instructor"),
            "can_enroll": (role == "student" and courses.count() == 0),
            "courses": serializer.data,
        })
    

class ModuleViewSet(viewsets.ModelViewSet):
    serializer_class = ModuleModelSerializer
    permission_classes = [IsInstructorOrAdmin]

    def get_queryset(self):
        course_id = self.kwargs.get("course_pk")
        return Module.objects.filter(course_id=course_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        course_id = self.kwargs.get("course_pk")
        course = Course.objects.filter(id=course_id).first()
        course_title = course.title if course else None

        return Response({
            "course_id": course_id,
            "course_title": course_title,
            "total_modules": queryset.count(),
            "can_edit": request.user.is_staff 
                        or request.user.is_superuser 
                        or getattr(request.user, "role", None) == "instructor",
            "modules": serializer.data,
        })        


class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonModelSerializer
    permission_classes = [IsInstructorOrAdmin]

    def get_queryset(self):
        module_id = self.kwargs.get("module_pk")
        return Lesson.objects.filter(module_id=module_id)
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        module_id = self.kwargs.get("module_pk")
        module = Module.objects.filter(id=module_id).first()
        module_title = module.title if module else None
        return Response({
            "module_id": module_id,
            "module_title": module_title,
            "total_lessons": queryset.count(),
            "can_edit": request.user.is_staff or request.user.is_superuser or getattr(request.user, "role", None) == "instructor",
            "lessons": serializer.data,
        })

