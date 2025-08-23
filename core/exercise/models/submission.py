from __future__ import annotations
from django.db import models
from .exercises import Exercise
from exercise.exercise_choises import SubmissionsStatus
from user.models import MyUser


class Submission(models.Model):
    exercise = models.ForeignKey(
            Exercise,
            related_name='submissions',
            on_delete=models.CASCADE,
            verbose_name='Задание'
            )

    student = models.ForeignKey(
            MyUser,
            on_delete=models.CASCADE,
            related_name='submissions',
            verbose_name='Студент'
            )

    attempt_no = models.PositiveSmallIntegerField(
            default=1,
            verbose_name='Попытка'
            )

    content = models.TextField(
            verbose_name='Решение'
            )

    status = models.CharField(
            choices=SubmissionsStatus.choices,
            default=SubmissionsStatus.SUBMITTED,
            verbose_name='Статус'
            )

    created_at = models.DateTimeField(
            auto_now_add=True,
            verbose_name='Дата создания'
            )

    updated_at = models.DateTimeField(
            auto_now=True,
            verbose_name='Дата изменения'
            )
    
    def save(self, *args, **kwargs):
        if not self.pk:
            last_submission = Submission.objects.filter(
                exercise=self.exercise,
                student=self.student
            ).order_by("-attempt_no").first()

            if last_submission:
                self.attempt_no = last_submission.attempt_no + 1
            else:
                self.attempt_no = 1

        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.content

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["exercise", "student", "attempt_no"],
                name="uniq_submission_attempt"
            )
        ]
        indexes = [
            models.Index(fields=["exercise", "student", "attempt_no"]),
            models.Index(fields=["student", "exercise"]),
        ]
        verbose_name = 'Решение'
        verbose_name_plural = 'Решения'
  
