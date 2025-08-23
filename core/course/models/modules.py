from __future__ import annotations
from django.db import models
from .course import Course


class Module(models.Model):
    title  = models.CharField(
            max_length=50,
            verbose_name='Название темы'
            )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='modules',
        verbose_name='Курс'
            )

    position = models.PositiveSmallIntegerField(
            verbose_name='Номер темы'
            )

    description = models.TextField(
            verbose_name='Описание темы'
            )

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Тема курса'
        verbose_name_plural = 'Темы курса'

