from django.contrib import admin
from course.models.course import Course
from course.models.modules import Module
from course.models.lessons import Lesson 
from course.models.attendance import Attendance
from course.models.shedule_session import SheduleSession
from course.models.course_instructor import CourseInstructor
from course.models.course_student import CourseStudent


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'is_active', 'duration'] 
    list_filter = ['is_active']
    search_fields = ['title', 'price', 'duration']


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'course', 'position']
    list_filter = ['position']
    search_fields = ['title', 'position']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'module', 'position']
    list_filter = ['position']
    search_fields = ['position', 'title']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'shedule_session', 'status', 'comment']
    list_filter = ['status']
    search_fields = ['status', 'comment']


@admin.register(SheduleSession)
class SheduleSessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'course', 'module', 'lesson', 'starts_at', 'end_at', 'session_type']
    list_filter = ['module', 'session_type']
    search_fields = ['module', 'session_type']


@admin.register(CourseInstructor)
class CourseInstructorAdmin(admin.ModelAdmin):
    list_display = ['id', 'instructor', 'course']
    search_fields = ['instructor', 'course']
    list_filter = ['course']


@admin.register(CourseStudent)
class CourseStudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'course', 'status']
    search_fields = ['user', 'course', 'status']
    list_filter = ['status']

