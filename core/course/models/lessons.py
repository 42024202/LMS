from __future__ import annotations
from django.db import models
from .modules import Module


class Lesson(models.Model):
    title = models.CharField(
            max_length=50,
            verbose_name='Заголовок урока'
            )

    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Тема курса'
            )
    
    content = models.TextField(
        verbose_name='Содержание урока'
            )

    position = models.PositiveSmallIntegerField(
        verbose_name='Номер урока'
            )

    starts_at = models.DateTimeField(
        verbose_name='Начало урока'
            )

    end_at = models.DateTimeField(
        verbose_name='Конец урока'
            )
    
    meeting_url = models.TextField(
        default=None,
        blank=True,
        null=True,
        verbose_name='Ссылка на встречу'
            )

    description = models.TextField(
        verbose_name='Описание урока'
            )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

