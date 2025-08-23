from django.urls import path, include
from rest_framework.routers import DefaultRouter
from course.views.index_view import CourseViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
    # все урлы из CourseViewSet
    path("", include(router.urls)),
]

