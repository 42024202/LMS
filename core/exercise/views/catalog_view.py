from rest_framework import viewsets, permissions
from rest_framework.response import Response
from exercise.models.exercises import Exercise
from exercise.models.submission import Submission
from exercise.models.grade import Grade
from exercise.exercise_serializers.grade_serializer import GradeModelSerializer
from exercise.exercise_serializers.submission_serializer import SubmissionModelSerializer
from exercise.exercise_serializers.exercise_serializer import ExerciseModelSerializer
from common.permissions import StudentSubmission, IsInstructorOrAdmin
from django.shortcuts import get_object_or_404


class ExerciseViewSet(viewsets.ModelViewSet):
    serializer_class = ExerciseModelSerializer 
    permission_classes = [IsInstructorOrAdmin]

    def get_queryset(self):
        lesson_id = self.kwargs.get("lesson_pk")
        return Exercise.objects.filter(lesson_id=lesson_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        lesson_id = self.kwargs.get("lesson_pk")
        lesson_title = None
        if lesson_id:
            lesson_title = Exercise.objects.filter(lesson_id=lesson_id).first().lesson.title
        return Response({
            "lesson_title": lesson_title,
            "total_exercises": queryset.count(),
            "can_edit": self.request.user.is_staff or request.user.is_superuser or getattr(request.user, "role", None) == "instructor",
            "exercises": serializer.data,
                    })


class SubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = SubmissionModelSerializer
    permission_classes = [StudentSubmission]

    def get_queryset(self):
        exercise_id = self.kwargs.get("exercise_pk")

        if self.request.user.is_superuser or self.request.user.is_staff or getattr(self.request.user, "role", None) == "instructor":
            return Submission.objects.filter(
                    exercise_id=exercise_id
                    )

        return Submission.objects.filter(
                exercise_id=exercise_id,
                student=self.request.user
                )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        exercise_id = self.kwargs.get("exercise_pk")
        exercise = get_object_or_404(Exercise, id=exercise_id)
        exercise_title = exercise.title
        return Response({
            "exercise_title": exercise_title,
            "total_submissions": queryset.count(),
            "can_edit": True,
            "submissions": serializer.data,
                        })


class GradeViewSet(viewsets.ModelViewSet):
    serializer_class = GradeModelSerializer
    permission_classes = [IsInstructorOrAdmin]

    def get_queryset(self):
        submission_id = self.kwargs.get("submission_pk")
        return Grade.objects.filter(submission_id=submission_id)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        submission_id = self.kwargs.get("submission_pk")
        submission = get_object_or_404(Submission, id=submission_id)
        return Response({
            "submission_id": submission_id,
            "submission_content": submission.content,
            "total_grades": queryset.count(),
            "can_edit": self.request.user.is_staff or request.user.is_superuser or getattr(request.user, "role", None) == "instructor",
            "grades": serializer.data,
                        })

