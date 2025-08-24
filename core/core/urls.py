from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers

from course.views.index_view import CourseViewSet, ModuleViewSet, LessonViewSet
from exercise.views.catalog_view import ExerciseViewSet, SubmissionViewSet, GradeViewSet
from exercise.views.course_grades import StudentCourseGradesViewSet
from course.views.course_attendance import StudentCourseAttendanceViewSet

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# ---- Базовый роутер ----
router = routers.SimpleRouter()
router.register(r'courses', CourseViewSet, basename='course')

# ---- Вложенные роутеры (макс. 3 уровня) ---
# /api/courses/{course_id}/modules/

courses_router = routers.NestedSimpleRouter(router, r'courses', lookup='course')
courses_router.register(r'modules', ModuleViewSet, basename='course-modules')

course_router = routers.NestedSimpleRouter(router, r'courses', lookup='course')
course_router.register(r'grades', StudentCourseGradesViewSet, basename="course-grades")


# /api/modules/{module_id}/lessons/
modules_router = routers.NestedSimpleRouter(courses_router, r'modules', lookup='module')
modules_router.register(r'lessons', LessonViewSet, basename='module-lessons')

# /api/lessons/{lesson_id}/exercises/
lessons_router = routers.NestedSimpleRouter(modules_router, r'lessons', lookup='lesson')
lessons_router.register(r'exercises', ExerciseViewSet, basename='lesson-exercises')
# ---- Grades по курсу ----
grades_router = routers.NestedSimpleRouter(router, r'courses', lookup='course')
grades_router.register(r'grades', StudentCourseGradesViewSet, basename="course-grades")

# ---- Submissions → Grades ----
exercises_router = routers.NestedSimpleRouter(lessons_router, r'exercises', lookup='exercise')
exercises_router.register(r'submissions', SubmissionViewSet, basename='exercise-submissions')

submissions_router = routers.NestedSimpleRouter(exercises_router, r'submissions', lookup='submission')
submissions_router.register(r'grades', GradeViewSet, basename='submission-grades')

attendance_router = routers.NestedSimpleRouter(router, r'courses', lookup='course')
attendance_router.register(r'attendance', StudentCourseAttendanceViewSet, basename='course-attendance')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('user.urls')),
    path('api/library/', include('library.urls')),
    path('api/payment/', include('payment.urls')),

    path("api/", include(router.urls)),
    path("api/", include(courses_router.urls)),
    path("api/", include(course_router.urls)),
    path("api/", include(attendance_router.urls)),
    path("api/", include(modules_router.urls)),
    path("api/", include(lessons_router.urls)),
    path("api/", include(grades_router.urls)),
    path("api/", include(exercises_router.urls)),
    path("api/", include(submissions_router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
#handler404 = NotFoundView.as_view()

