from __future__ import annotations
from django.db import models
from .course import Course
from user.models import MyUser


class CourseInstructor(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='instructors',
        verbose_name='Курс'
            )

    instructor = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='teaching_courses',
        verbose_name='Инструктор'
            )
    def __str__(self):
        return f'{self.instructor} - {self.course}'

    class Meta:
        verbose_name = 'Инструктор'
        verbose_name_plural = 'Инструкторы'

