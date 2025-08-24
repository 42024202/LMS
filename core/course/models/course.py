from __future__ import annotations
from django.db import models 
from django.core.validators import MinValueValidator


class Course(models.Model):
    title = models.CharField(
            max_length=50,
            verbose_name='Название курса'
            )

    author = models.CharField(
            max_length=50,
            blank=True,
            null=True,
            verbose_name='Автор курса'
            )
    price = models.DecimalField(
            max_digits=10,
            decimal_places=2,
            validators=[MinValueValidator(0)],
            verbose_name='Цена'
            )

    duration = models.PositiveSmallIntegerField(
            verbose_name='Длительность курса в месяцах'
            )
    
    starts_at = models.DateField(
            blank=True,
            null=True,
            verbose_name='Начало курса',
            default=None
            )

    end_at = models.DateField(
            blank=True,
            null=True,
            default=None,
            verbose_name='Конец курса'
            )

    is_active = models.BooleanField(
            default=True,
            verbose_name='Активен ли курс'
            )

    created_at = models.DateTimeField(
            auto_now_add=True,
            verbose_name='Дата создания'
            )

    description = models.TextField(
            verbose_name='Описание курса'
            )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

