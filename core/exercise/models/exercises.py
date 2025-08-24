from __future__ import annotations
from django.db import models
from course.models.lessons import Lesson
from exercise.exercise_choises import ExerciseStatus


class Exercise(models.Model):
    lesson = models.ForeignKey(
            Lesson,
            on_delete=models.CASCADE,
            related_name='exercises',
            verbose_name='Урок'
            )

    title = models.CharField(
            max_length=50,
            verbose_name='Название задания'
            )

    description = models.TextField(
            verbose_name='Описание задания'
            )
    
    due_at = models.DateTimeField(
            auto_now_add=True,
            verbose_name='Срок выполнения'
            )

    status = models.CharField(
            max_length=50,
            choices=ExerciseStatus.choices,
            default=ExerciseStatus.ACTIVE,
            verbose_name='Статус задания'
            )

    max_score = models.PositiveSmallIntegerField(
            default=100,
            verbose_name='Максимальный балл'
            )

    sample_solution = models.TextField(
            verbose_name='Пример решения'
            )
    
    created_at = models.DateTimeField(
            auto_now_add=True,
            verbose_name='Дата создания'
            )

    updated_at = models.DateTimeField(
            auto_now=True,
            verbose_name='Дата обновления'
            )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'

