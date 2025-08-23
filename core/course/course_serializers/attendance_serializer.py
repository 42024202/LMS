from rest_framework import serializers
from course.models.attendance import Attendance
from course.models.shedule_session import SheduleSession


class SheduleSessionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SheduleSession
        fields = (
            "id",
            "course",
            "module",
            "lesson",
            "instructor",
            "starts_at",
            "end_at",
            "session_type",
        )


class AttendanceModelSerializer(serializers.ModelSerializer):
    student_username = serializers.SerializerMethodField()
    course_title = serializers.SerializerMethodField()
    module_title = serializers.SerializerMethodField()
    lesson_title = serializers.SerializerMethodField()
    shedule_session_id = serializers.PrimaryKeyRelatedField(
        queryset=SheduleSession.objects.all(),
        source="shedule_session",
        write_only=True
    )

    class Meta:
        model = Attendance
        fields = (
            "id",
            "student",
            "student_username",        # красивое имя
            "status",
            "comment",
            "shedule_session_id",
            "course_title",
            "module_title",
            "lesson_title",
        )

    def get_student_username(self, obj):
        # obj.student.user — это объект MyUser
        user = obj.student.user
        return getattr(user, "username", None)
    def get_course_title(self, obj):
        return obj.shedule_session.course.title if obj.shedule_session and obj.shedule_session.course else None

    def get_module_title(self, obj):
        return obj.shedule_session.lesson.module.title if obj.shedule_session and obj.shedule_session.lesson else None

    def get_lesson_title(self, obj):
        return obj.shedule_session.lesson.title if obj.shedule_session and obj.shedule_session.lesson else None

