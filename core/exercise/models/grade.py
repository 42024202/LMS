from __future__ import annotations
from django.db import models
from .submission import Submission
from django.core.validators import MinValueValidator, MaxValueValidator
from user.models import MyUser


class Grade(models.Model):
    submission = models.ForeignKey(
            Submission,
            on_delete=models.CASCADE,
            related_name='grades',
            verbose_name='Решение'
            )

    student = models.ForeignKey(
            MyUser,
            on_delete=models.CASCADE,
            related_name='grades',
            verbose_name='Студент'
            )

    score = models.PositiveSmallIntegerField(
            verbose_name='Оценка',
            validators=[MinValueValidator(0), MaxValueValidator(100)]
            )

    feedback = models.TextField(
            verbose_name='Комментарий'
            )
    
    grade_at = models.DateTimeField(
            auto_now_add=True,
            verbose_name='Когда оценено'
            )

    def __str__(self):
        return f'{self.submission} - {self.score}'

    class Meta:
        verbose_name = 'Оценка задания'
        verbose_name_plural = 'Оценки заданий'

